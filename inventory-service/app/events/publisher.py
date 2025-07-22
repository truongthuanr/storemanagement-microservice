# app/events/publisher.py
import aio_pika, json
from datetime import datetime

async def publish_event(
    routing_key: str,
    event: str,
    data: dict,
    correlation_id: str = None,
    producer: str = "inventory-service"
):
    message = {
        "event": event,
        "timestamp": datetime.utcnow().isoformat(),
        "correlation_id": correlation_id,
        "producer": producer,
        "data": data,
    }

    conn = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    ch = await conn.channel()
    await ch.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key=routing_key
    )
    await conn.close()
