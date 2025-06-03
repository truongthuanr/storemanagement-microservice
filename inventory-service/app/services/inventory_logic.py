import grpc
from concurrent import futures

from app.proto import inventory_pb2, inventory_pb2_grpc
from app.models.inventory import Inventory
from app.database import SessionLocal
from app.crud.inventory_crud import get_inventory_by_id

class InventoryServiceImpl(inventory_pb2_grpc.InventoryServiceServicer):
    def __init__(self):
        self.db = SessionLocal()

    def GetInventory(self, request, context):
        product = get_inventory_by_id(request.product_id)
        return inventory_pb2.ProductResponse(
            product_id=product.id,
            stock=product.stock,
            price=float(product.price)
        )

    def GetStock(self, request, context):
        inventory_id = request.inventory_id
        item = self.db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
        if item is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Product {inventory_id} not found")
            return inventory_pb2.StockResponse()

        return inventory_pb2.StockResponse(
            product_id=item.inventory_id,
            stock=item.stock,
            price=item.price
        )

    def UpdateStock(self, request, context):
        inventory_id = request.inventory_id
        delta = request.delta

        item = self.db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
        if item is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Inventory {inventory_id} not found")
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
