# app/services/publisher_adapter.py
from typing import Any, Dict
import aio_pika
from fastapi import FastAPI
from app.brokers.publisher import publish_event
from app.servicelogging.servicelogger import logger

class PublisherAdapter:
    def __init__(self, app: FastAPI):
        self.app = app

    async def publish(self, routing_key: str, message: Dict[str, Any]) -> None:
        """
        Publish message to RabbitMQ via app.state.rabbitmq_exchange.
        """
        try:
            exchange: aio_pika.Exchange = self.app.state.rabbitmq_exchange
            await publish_event(exchange, routing_key, message)
            logger.info(
                f"[PublisherAdapter] Published event `{routing_key}` "
                f"with correlation_id={message.get('correlation_id')}"
            )
        except Exception:
            logger.exception(
                f"[PublisherAdapter] Failed to publish event `{routing_key}`"
            )
            raise
