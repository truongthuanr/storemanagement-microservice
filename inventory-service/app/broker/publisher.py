# app/broker/publisher.py
import aio_pika
import json
from app.broker.rabbitmq import get_channel
from app.servicelogging.servicelogger import logger

async def publish_event(routing_key: str, message: dict):
    """
    Publish a fully-built message (already includes event, timestamp, etc.)
    to the given routing_key.
    """
    ch = await get_channel()
    await ch.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message, default=str).encode(),
            content_type="application/json"
        ),
        routing_key=routing_key
    )
    logger.info(f"📤 Published message to `{routing_key}`")
