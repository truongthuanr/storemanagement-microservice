# brokers/rabbitmq.py
import os
from contextlib import asynccontextmanager
import aio_pika
# from app.consumers.rabbitmq import get_rabbitmq_url
# from app.pr.price_consumer import handle_price_updated

# @asynccontextmanager
# async def lifespan(app):
#     rabbitmq_url = get_rabbitmq_url()
#     connection = await aio_pika.connect_robust(rabbitmq_url)
#     channel = await connection.channel()
#     exchange = await channel.declare_exchange("order.exchange", aio_pika.ExchangeType.DIRECT, durable=True)

#     app.state.rabbitmq_channel = channel
#     app.state.rabbitmq_exchange = exchange
    
#     # price update consume
#     # Declare queue cho order-service
#     order_reserved_queue = await channel.declare_queue(
#         "order-service.inventory_reserved",  # queue dành riêng cho order-service
#         durable=True
#     )
#     # Bind queue với routing key
#     await order_reserved_queue.bind(exchange, routing_key="order.inventory_reserved")
#     await order_reserved_queue.consume(handle_stock_reserved_updated)
#     print("✅ Consumer started")
    
#     yield

#     await connection.close()
#     print("🛑 Consumer stopped")

def get_rabbitmq_url() -> str:
    return os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

async def get_connection() -> aio_pika.RobustConnection:
    """
    Create and return a robust RabbitMQ connection.
    """
    url = get_rabbitmq_url()
    return await aio_pika.connect_robust(url)

async def get_channel(connection: aio_pika.RobustConnection) -> aio_pika.Channel:
    """
    Create and return a channel from the given connection.
    """
    return await connection.channel()

async def get_exchange(channel: aio_pika.Channel) -> aio_pika.Exchange:
    """
    Declare and return the exchange for the order service.
    """
    return await channel.declare_exchange(
        "order.exchange",
        aio_pika.ExchangeType.DIRECT,
        durable=True
    )