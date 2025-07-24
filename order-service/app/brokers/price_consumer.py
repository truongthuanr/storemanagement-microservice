# consumers/price_consumer.py
import aio_pika
import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product_price import ProductPrice
from datetime import datetime



# async def handle_price_updated(msg: aio_pika.IncomingMessage):
#     async with msg.process():
#         data = json.loads(msg.body)
#         product_id = data["product_id"]
#         price = data["price"]
#         updated_at = datetime.fromisoformat(data["updated_at"])

#         db: Session = SessionLocal()
#         existing = db.query(ProductPrice).filter_by(product_id=product_id).first()
#         if existing:
#             existing.price = price
#             existing.updated_at = updated_at
#         else:
#             db.add(ProductPrice(
#                 product_id=product_id,
#                 price=price,
#                 updated_at=updated_at
#             ))
#         db.commit()
#         db.close()
