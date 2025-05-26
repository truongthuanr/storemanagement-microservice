import grpc
from concurrent import futures

from app.proto import inventory_pb2, inventory_pb2_grpc
from app.models.product import Product
from app.database import SessionLocal

class InventoryServiceImpl(inventory_pb2_grpc.InventoryServiceServicer):
    def __init__(self):
        self.db = SessionLocal()

    def GetStock(self, request, context):
        product_id = request.product_id
        item = self.db.query(Product).filter(Product.product_id == product_id).first()
        if item is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Product {product_id} not found")
            return inventory_pb2.StockResponse()

        return inventory_pb2.StockResponse(
            product_id=item.product_id,
            stock=item.stock,
            price=item.price
        )

    def UpdateStock(self, request, context):
        product_id = request.product_id
        delta = request.delta

        item = self.db.query(Product).filter(Product.product_id == product_id).first()
        if item is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Product {product_id} not found")
            return inventory_pb2.StockResponse()

        item.stock += delta
        if item.stock < 0:
            item.stock = 0

        self.db.commit()
        self.db.refresh(item)

        return inventory_pb2.StockResponse(
            product_id=item.product_id,
            stock=item.stock,
            price=item.price
        )
