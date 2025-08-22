from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker
from app.core.config import settings

broker_notify = RabbitBroker(url=settings.RABBITMQ_URL)

exch_notify = RabbitExchange('exch_notify', durable=True)

q_notify = RabbitQueue('q_notify', durable=True)

