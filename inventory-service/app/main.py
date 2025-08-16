# app/main.py
import sys
import os
import asyncio
from app.database import Base, engine
from app.models import inventory  # import models to ensure table creation
from app.grpc.grpc_server import serve_grpc
from app.broker.consumer import consume
from app.servicelogging.servicelogger import logger


def setup_paths():
    """Ensure proto/ directory is importable."""
    BASE_DIR = os.path.dirname(__file__)
    PROTO_DIR = os.path.join(BASE_DIR, "proto")
    if PROTO_DIR not in sys.path:
        sys.path.append(PROTO_DIR)


def init_db():
    """Initialize database schema."""
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database initialized")


async def main():
    """Run both gRPC server and RabbitMQ consumer concurrently."""
    # Run consumer & gRPC server in parallel
    consumer_task = asyncio.create_task(consume())
    grpc_task = asyncio.create_task(serve_grpc())

    logger.info("🚀 Inventory Service started")

    # Wait until one of the tasks exits (or raises)
    await asyncio.gather(grpc_task, consumer_task)


if __name__ == "__main__":
    setup_paths()
    init_db()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Inventory Service stopped by user")
    except Exception as e:
        logger.exception(f"❌ Inventory Service crashed: {e}")
