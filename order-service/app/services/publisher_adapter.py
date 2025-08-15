# app/services/publisher_adapter.py
from typing import Any, Dict
from fastapi import FastAPI
from app.brokers.publish_order_created import publish_order_created
from app.servicelogging.servicelogger import logger

class PublisherAdapter:
    def __init__(self, app: FastAPI):
        self.app = app

    async def publish(self, event: str, message: Dict[str, Any]) -> None:
        # Bạn có thể mở rộng để log, retry, enrich message...
        await publish_order_created(self.app, message)
        logger.info(f"[PublisherAdapter] Received event={event}")

