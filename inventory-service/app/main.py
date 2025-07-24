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
from app.broker.consumer import consume

Base.metadata.create_all(bind=engine)

async def main():
    consumer_task = asyncio.create_task(consume())
    grpc_task = asyncio.create_task(serve_grpc())
    
    # Wait for both to finish (hoặc bất kỳ cái nào raise exception)
    await asyncio.gather(grpc_task, consumer_task)

if __name__ == "__main__":
    print("🚀 Starting Inventory Service...", flush=True)
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
