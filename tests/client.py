import asyncio

from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker, ExchangeType

from app.core.config import settings
from app.schemas.user import NotifyEmailEventType

broker = RabbitBroker(url=settings.RABBITMQ_URL)

exchange = RabbitExchange('notify', type=ExchangeType.TOPIC, durable=True)

q_email = RabbitQueue('notify.email', durable=True, routing_key='notify.*.email')


async def test_publish():
    msg = {
     "payload": {
        "email": "a.bojic22@gmail.com",
        "first_name": "Alice",
        "last_name": "Doe",
        "language": "ru",
        "login": "alice_login",
         "password": "1234",
        "confirm_url": "https://app.example.com/confirm",
     }
     }
    async with broker:
        await broker.publish(
            message=msg,
            exchange=exchange,
            content_type="application/json",
            routing_key=NotifyEmailEventType.USER_REGISTERED.value
        )
        print("Message published")


def run():
    asyncio.run(test_publish())

if __name__ == '__main__':
    run()
