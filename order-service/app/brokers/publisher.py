# brokers/publisher.py
import json
import aio_pika
from app.servicelogging.servicelogger import logger

async def publish_event(
    exchange: aio_pika.Exchange,
    routing_key: str,
    message: dict
):
    """
    Publish an event to the given routing_key via RabbitMQ exchange.
    """
    try:
        body = json.dumps(message).encode()

        await exchange.publish(
            aio_pika.Message(
                body=body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
            ),
            routing_key=routing_key,
        )

        logger.info(
            f"📤 Published event `{routing_key}` "
            f"with correlation_id={message.get('correlation_id')}"
        )
    except Exception:
        logger.exception(f"❌ Failed to publish event `{routing_key}`")
        raise
