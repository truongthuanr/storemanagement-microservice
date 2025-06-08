# server.py
import sys
import os

BASE_DIR = os.path.dirname(__file__)
# Thêm thư mục 'proto/' vào sys.path
PROTO_DIR = os.path.join(BASE_DIR, "proto")
sys.path.append(PROTO_DIR)

from concurrent import futures
import grpc
from app.services.inventory_logic import InventoryServiceImpl
from app.proto import inventory_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServiceImpl(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("✅ Inventory gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
