import grpc
from app.proto import inventory_pb2, inventory_pb2_grpc

class InventoryClient:
    def __init__(self, host="inventory-service", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = inventory_pb2_grpc.InventoryServiceStub(self.channel)

    def get_inventory(self, product_id: int):
        # request theo protobuf model
        request = inventory_pb2.ProductRequest(id=product_id)
        response = self.stub.GetInventory(request)
        return {
            "id": response.id,
            "name": response.name,
            "description": response.description,
            "price": float(response.price),
            "stock": response.stock
        }

    def update_inventory(self, product_id: int, new_stock: int):
        # tạo ProductUpdateRequest theo protobuf model
        product = inventory_pb2.Product(
            id=product_id,
            stock=new_stock,
            # nếu các trường khác cần update thì thêm ở đây
        )
        request = inventory_pb2.ProductUpdateRequest(product=product)
        response = self.stub.UpdateInventory(request)
        return {
            "id": response.product.id,
            "name": response.product.name,
            "description": response.product.description,
            "price": float(response.product.price),
            "stock": response.product.stock
        }
