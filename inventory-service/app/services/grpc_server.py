import grpc
from concurrent import futures

from app.proto import inventory_pb2_grpc
from app.services.inventory_logic import InventoryServiceImpl  

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServiceImpl(), server)
    server.add_insecure_port("[::]:50051")  # Cổng gRPC của Inventory Service
    server.start()
    server.wait_for_termination()
