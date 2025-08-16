from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timezone
from fastapi import Request
import json


from app import crud, schemas
from app.database.database import SessionLocal
from app.crud import order_crud, orderitem_crud
from app.models.order_model import Order, OrderStatusEnum
from app.models.orderitem_model import OrderItem
from app.schemas.order_schema import OrderCreate
from app.exceptions.order_exception import OrderValidationError, ProductUnavailable

from app.servicelogging.servicelogger import logger

# Message format
# {
#   "event": "order.inventory_reserved",
#   "timestamp": "...",
#   "correlation_id": "...",
#   "producer": "inventory-service",
#   "order_id": 123,
#   "status": "reserved",   // or "failed"
#   "items": [ ... ],
#   "reason": "..."
# }
class OrderService:
    def __init__(self, publisher, producer_name: str = "order-service"):
        self.publisher = publisher
        self.producer = producer_name

    async def create_order(self, db: Session, payload: OrderCreate) -> dict:
        logger.info(f"Start create_order for customer_id={payload.customer_id} with {len(payload.items)} items.")

        if not payload.items:
            raise OrderValidationError("Order must contain at least one item")

        # Step 1: Ghi Order
        order = Order(
            customer_id=payload.customer_id,
            status=OrderStatusEnum.init.value,
            created_at=datetime.now(timezone.utc)
        )
        db.add(order)
        db.flush()
        logger.info(f"Created order with id={order.id}, status={order.status}")

        # Step 2: Ghi OrderItems
        for item in payload.items:
            db_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_per_unit=None
            )
            db.add(db_item)
        db.commit()
        logger.info(f"Committed order and items to DB for order_id={order.id}")

        # Step 3: Gửi message
        correlation_id = str(uuid4())
        message = {
            "event": "order.created",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "correlation_id": correlation_id,
            "producer": self.producer,
            "data": {
                "order_id": str(order.id),
                "user_id": payload.customer_id,
                "items": [
                    {"product_id": item.product_id, "quantity": item.quantity}
                    for item in payload.items
                ]
            }
        }

        logger.info(f"Publishing order.created message for order_id={order.id}, correlation_id={correlation_id}")
        await self.publisher.publish("order.created", message)
        logger.info(f"Message published successfully for order_id={order.id}")

        return {
            "order_id": order.id,
            "status": order.status,
            "correlation_id": correlation_id
        }
    
    async def handle_stock_reserved_updated(self, message):
        async with message.process():
            try:
                payload = json.loads(message.body)
                order_id = int(payload["order_id"])
                success = payload.get("status") == "reserved"
                reserved_items = payload.get("items", [])
                reason = payload.get("reason")
                
                with SessionLocal() as db:   # session per message
                    try:
                        order = order_crud.set_order_status(db, order_id, success, reason)
                        if order and success and reserved_items:
                            orderitem_crud.update_reserved_items(db, order_id, reserved_items)
                        db.commit()
                    except:
                        db.rollback()
                        raise
                    if not order:
                        logger.warning(f"[Consumer] Order {order_id} not found")
                    elif success:
                        logger.info(f"[Consumer] Order {order_id} confirmed")
                    else:
                        logger.info(f"[Consumer] Order {order_id} cancelled, reason={reason}")

            except Exception as e:
                logger.exception(f"❌ Failed to process inventory_reserved: {e}")
                raise

    def get_order(self, db: Session, order_id: int):
        return crud.order.get_order(db, order_id)

    def list_orders(self, db: Session):
        return crud.order.list_orders(db)

    def delete_order(self, db: Session, order_id: int) -> bool:
        return crud.order.delete_order(db, order_id)