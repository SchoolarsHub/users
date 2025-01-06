import aio_pika
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue
from faststream.rabbit import RabbitBroker as Broker
from faststream.rabbit.annotations import RabbitBroker

from app.infrastructure.brokers.rabbit.config import RabbitConfig


class AMQPBroker:
    def __init__(self, config: RabbitConfig) -> None:
        self.config = config

    async def _declare_amqp_exchange(self, broker: RabbitBroker) -> aio_pika.RobustExchange:
        exchange = await broker.declare_exchange(exchange=RabbitExchange(type=ExchangeType.DIRECT, name=self.config.exchange, durable=True))
        return exchange

    async def _declare_amqp_queue(self, broker: RabbitBroker) -> aio_pika.RobustQueue:
        queue = await broker.declare_queue(queue=RabbitQueue(name=self.config.queue, durable=True))
        return queue

    async def _bind_queue_to_exchange(self, queue: aio_pika.RobustQueue, exchange: aio_pika.RobustExchange) -> None:
        await queue.bind(exchange=exchange, routing_key=queue.name)

    async def _startup_broker(self, broker: RabbitBroker) -> None:
        await broker.start()

    async def setup_amqp(self) -> RabbitBroker:
        broker = Broker(url=self.config.rabbit_url)

        await self._startup_broker(broker=broker)

        exchange = await self._declare_amqp_exchange(broker=broker)
        queue = await self._declare_amqp_queue(broker=broker)
        await self._bind_queue_to_exchange(queue=queue, exchange=exchange)

        return broker


async def setup_amqp_broker(amqp_broker: AMQPBroker) -> RabbitBroker:
    return await amqp_broker.setup_amqp()
