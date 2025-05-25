import grpc
from app.proto import inventory_pb2, inventory_pb2_grpc

def get_inventory(product_id: int):
    with grpc.insecure_channel("inventory-service:50051") as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        request = inventory_pb2.InventoryRequest(product_id=product_id)
        return stub.GetInventory(request)
