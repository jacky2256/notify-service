import asyncio
import json

from faststream import FastStream, Depends
from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker, ExchangeType, RabbitMessage

from app.core.config import settings
from app.core.log_utils import logger
from app.services.email import EmailService
from app.dependencies import get_email_service
from app.schemas.user import NotifyEmailEventType, RegisteredPayload, PassResetPayload, PassChangedPayload

broker = RabbitBroker(url=settings.RABBITMQ_URL)

exchange = RabbitExchange('notify', type=ExchangeType.TOPIC, durable=True)
dlx = RabbitExchange("dead.letters", type=ExchangeType.TOPIC, durable=True)

dlq_notify = RabbitQueue(name="notify.dead.letters", durable=True, routing_key="notify",
                         arguments={"x-message-ttl": settings.DLQ_TTL_SECONDS},
                         )
q_email = RabbitQueue('notify.email', durable=True, routing_key='notify.#.email',
                      arguments={"x-dead-letter-exchange": "dead.letters",
                                 "x-dead-letter-routing-key": "notify"}
                      )

app = FastStream(broker)

@broker.subscriber(q_email, exchange)
async def notify_email(
    msg: RabbitMessage,
    email_service: EmailService = Depends(get_email_service),
):
    try:
        routing_key = msg.raw_message.routing_key
        body = json.loads(msg.body)
        payload = body["payload"]

        if routing_key == NotifyEmailEventType.USER_REGISTERED:
            user_info = RegisteredPayload.model_validate(payload)
            await email_service.send_registration_credentials(user_info)
        elif routing_key == NotifyEmailEventType.USER_PASS_RESET:
            user_info = PassResetPayload.model_validate(payload)
            await email_service.send_reset_password(user_info)
        elif routing_key == NotifyEmailEventType.USER_PASS_CHANGED:
            user_info = PassChangedPayload.model_validate(payload)
            await email_service.send_password_changed_success(user_info)

        await msg.ack()

    except Exception as e:
        print(e)
        await msg.reject()

@broker.subscriber(queue=dlq_notify, exchange=dlx)
async def handle_dead_letters(msg: RabbitMessage):
    body = (
        json.loads(msg.body) if isinstance(msg.body, (bytes, bytearray))
        else msg.body
    )

    headers = msg.headers or {}
    xdeath = headers.get("x-death") or []
    orig_exchange = orig_rk = reason = None
    orig_queue = None

    if isinstance(xdeath, list) and xdeath:
        last = xdeath[0]
        orig_exchange = last.get("exchange")
        orig_queue = last.get("queue")
        orig_rk = (last.get("routing-keys") or [None])[0]
        reason = last.get("reason")

    log_data = {
        "reason": reason or "unknown",
        "exchange": orig_exchange or "unknown",
        "queue": orig_queue or "unknown",
        "routing_key": orig_rk or "unknown",
        "body": body,
    }

    logger.bind(**log_data).info("Dead letter received")

    await msg.ack()

async def run_consumer():
    await app.run()


if __name__ == '__main__':
    asyncio.run(run_consumer())
