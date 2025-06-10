# app/events/publisher.py
import aio_pika, json

async def publish_event(routing_key: str, message: dict):
    conn = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    ch = await conn.channel()
    await ch.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key=routing_key
    )
    await conn.close()
