# app/broker/consumer.py
import json
import aio_pika
from aio_pika import ExchangeType
from app.database import SessionLocal
from app.services import inventory_service as svc
from app.broker.publisher import publish_event
from app.broker.rabbitmq import get_connection, get_channel
from app.broker import _handle_order_created
from app.servicelogging.servicelogger import logger


async def consume():
    conn = await get_connection()
    ch = await get_channel()

    # Declare exchange
    exchange = await ch.declare_exchange("order.exchange", ExchangeType.DIRECT, durable=True)

    # Declare queue & bind
    queue = await ch.declare_queue("order.created", durable=True)
    await queue.bind(exchange, routing_key="order.created")

    # Start consuming
    await queue.consume(_handle_order_created)
    logger.info("📥 [MQ] Listening to queue `order.created`…")
