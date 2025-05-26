import grpc
from app.proto import inventory_pb2, inventory_pb2_grpc

class InventoryClient:
    def __init__(self, host="inventory-service", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = inventory_pb2_grpc.InventoryServiceStub(self.channel)

    def get_stock(self, product_id: int):
        request = inventory_pb2.StockRequest(product_id=product_id)
        response = self.stub.GetStock(request)
        return {
            "product_id": response.product_id,
            "stock": response.stock,
            "price": response.price
        }

    def update_stock(self, product_id: int, delta: int):
        request = inventory_pb2.UpdateStockRequest(product_id=product_id, delta=delta)
        response = self.stub.UpdateStock(request)
        return {
            "product_id": response.product_id,
            "stock": response.stock,
            "price": response.price
        }
