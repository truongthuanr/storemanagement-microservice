import grpc.aio
from app.proto import inventory_pb2, inventory_pb2_grpc

class InventoryClient:
    def __init__(self, host="inventory-service", port=50051):
        self.channel = grpc.aio.insecure_channel(f"{host}:{port}")
        self.stub = inventory_pb2_grpc.InventoryServiceStub(self.channel)

    async def get_inventory(self, product_id: int):
        request = inventory_pb2.InventoryRequestByProductId(product_id=product_id)
        response = await self.stub.GetInventoryByProductId(request)
        return {
            "product_id": response.product_id,
            "total_stock": response.total_stock
        }

    async def update_inventory(self, product_id: int, new_stock: int):
        product = inventory_pb2.Product(
            id=product_id,
            stock=new_stock,
            # TODO: bổ sung thêm trường nếu cần update
        )
        request = inventory_pb2.ProductUpdateRequest(product=product)
        response = await self.stub.UpdateInventory(request)
        return {
            "id": response.product.id,
            "name": response.product.name,
            "description": response.product.description,
            "price": float(response.product.price),
            "stock": response.product.stock
        }

    async def close(self):
        await self.channel.close()
