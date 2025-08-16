# app/broker/order_create_consumer.py
import aio_pika, json, asyncio
from datetime import datetime, timezone
from app.database import SessionLocal
from app.services import inventory_service as svc
from app.broker.publisher import publish_event
from aio_pika import ExchangeType

from app.servicelogging.servicelogger import logger
from app.schemas.inventory_response import InventoryResponseMessage, InventoryItemResult

# format request message:
# {
# "event": "order.created",
# "timestamp": "2025-07-18T14:00:00Z",
# "correlation_id": "abc123-xyz789",
# "producer": "order-service",
# "data": {
#     "order_id": "order_001",
#     "user_id": 123,
#     "items": [
#     { "product_id": 1, "quantity": 2 },
#     { "product_id": 2, "quantity": 1 }
#     ]
# }
# }

# Response message
# {
#   "event": "inventory.response",
#   "timestamp": "2025-07-23T21:15:35Z",
#   "correlation_id": "abc123",
#   "producer": "inventory-service",
#   "order_id": "ord_123456",
#   "status": "reserved",  // hoặc "failed"
#   "items": [
#     {
#       "product_id": 101,
#       "price": 15000
#     }
#   ],
#   "reason": null
# }

async def _handle_order_created(msg: aio_pika.IncomingMessage):
    async with msg.process():
        try:
            logger.debug(
                f"[order.created] Incoming message | "
                f"RoutingKey={msg.routing_key} | "
                f"Body={msg.body.decode('utf-8')}"
            )
            message = json.loads(msg.body)
            correlation_id = message["correlation_id"]
            payload = message["data"]
            await svc.handle_order_created(payload, correlation_id)
        except Exception as e:
            logger.exception(f"❌ Failed to process order.created: {e}")



