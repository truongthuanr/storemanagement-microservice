# app/broker/consumer.py
from app.broker.rabbitmq import get_channel, setup_exchange, EXCHANGE_NAME
from app.broker.order_create_consumer import _handle_order_created
from app.servicelogging.servicelogger import logger

async def consume():
    """Setup consumer for order.created events."""
    ch = await get_channel()
    exchange = await setup_exchange(ch)

    queue = await ch.declare_queue("order.created", durable=True)
    await queue.bind(exchange, routing_key="order.created")

    await queue.consume(_handle_order_created)
    logger.info(f"📥 [MQ] Listening on exchange `{EXCHANGE_NAME}` with queue `order.created`")