# brokers/rabbitmq.py
import os
from contextlib import asynccontextmanager
import aio_pika
# from app.consumers.rabbitmq import get_rabbitmq_url
# from app.pr.price_consumer import handle_price_updated

@asynccontextmanager
async def lifespan(app):
    rabbitmq_url = get_rabbitmq_url()
    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()
    exchange = await channel.declare_exchange("order.exchange", aio_pika.ExchangeType.DIRECT, durable=True)

    app.state.rabbitmq_channel = channel
    app.state.rabbitmq_exchange = exchange
    
    # price update consume
    # queue = await channel.declare_queue("price.updated", durable=True)
    # await queue.consume(handle_price_updated)
    print("✅ Consumer started")
    
    yield

    await connection.close()
    print("🛑 Consumer stopped")

def get_rabbitmq_url() -> str:
    return os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
