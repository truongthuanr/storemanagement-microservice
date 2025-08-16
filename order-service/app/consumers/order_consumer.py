# consumers/order_consumer.py
import json
import aio_pika
from app.services.order_service import OrderService

async def setup_order_consumer(
    channel: aio_pika.Channel,
    exchange: aio_pika.Exchange,
    order_service: OrderService
):
    queue = await channel.declare_queue(
        "order-service.inventory_reserved",
        durable=True,
    )
    await queue.bind(exchange, routing_key="order.inventory_reserved")
    await queue.consume(order_service.handle_stock_reserved_updated)
    print("✅ Consumer `order.inventory_reserved` started")