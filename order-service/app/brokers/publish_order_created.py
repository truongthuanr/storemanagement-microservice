# brokers/publish_order_created
import json
from fastapi import FastAPI
import aio_pika
from app.servicelogging.servicelogger import logger

async def publish_order_created(app: FastAPI, message: dict):
    try:
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
        logger.info(f"Published order.created with correlation_id={message.get('correlation_id')}")
    except Exception as e:
        logger.exception("❌ Failed to publish order.created message")
        raise