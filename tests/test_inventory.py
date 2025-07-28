import asyncio
import grpc
import inventory_pb2
import inventory_pb2_grpc

async def test_create_inventory():
    async with grpc.aio.insecure_channel('172.19.15.243:50051') as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)

        request = inventory_pb2.CreateInventoryRequest(
            name="Test Product",
            product_id = 3,
            description="A New Other product",
            price=129,
            stock=59
        )

        response = await stub.CreateInventory(request)
        print("CreateInventory Response:", response)

async def test_getinventory_byproductid():
    async with grpc.aio.insecure_channel('172.19.15.243:50051') as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        request = inventory_pb2.InventoryRequestByProductId(product_id=1)

        response= await stub.GetInventoryByProductId(request)
        print("Get Inventory by ProductId Response", response)

         # ✅ Assert kết quả đúng kiểu và hợp lệ
        assert isinstance(response.total_stock, int)
        assert response.total_stock >= 0


if __name__ == "__main__":
    # asyncio.run(test_create_inventory())
    asyncio.run(test_getinventory_byproductid())

