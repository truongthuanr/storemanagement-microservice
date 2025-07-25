import json
from fastapi import FastAPI
import aio_pika

async def publish_order_created(app: FastAPI, message: dict):
    body = json.dumps(message).encode()

    exchange: aio_pika.Exchange = app.state.rabbitmq_exchange

    await exchange.publish(
        aio_pika.Message(
            body=body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            content_type="application/json"
        ),
        routing_key="order.created"
    )
