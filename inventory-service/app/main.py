# app/main.py
import sys
import os
from database import Base, engine
from app.models.inventory import *

BASE_DIR = os.path.dirname(__file__)
# Thêm thư mục 'proto/' vào sys.path
PROTO_DIR = os.path.join(BASE_DIR, "proto")
sys.path.append(PROTO_DIR)

import asyncio
from app.grpc.grpc_server import serve_grpc
from app.events.consumer import consume

Base.metadata.create_all(bind=engine)

async def main():
    await asyncio.gather(
        serve_grpc(),   # chạy gRPC server
        consume()       # chạy RabbitMQ consumer
    )

if __name__ == "__main__":
    print("Starting Inventory Service...",flush=True)  # Thông báo bắt đầu chạy app
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error running Inventory Service: {e}",flush=True)
    else:
        print("Inventory Service exited cleanly.",flush=True)