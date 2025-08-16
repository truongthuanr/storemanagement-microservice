import json
import aio_pika
from app.broker.rabbitmq import get_channel, setup_exchange
from app.servicelogging.servicelogger import logger

async def publish_event(routing_key: str, message: dict):
    """Publish an event to the shared exchange."""
    ch = await get_channel()
    exchange = await setup_exchange(ch)

    await exchange.publish(
        aio_pika.Message(
            body=json.dumps(message, default=str).encode(),
            content_type="application/json"
        ),
        routing_key=routing_key
    )
    logger.info(f"📤 Published `{routing_key}` to exchange `{exchange.name}`")
