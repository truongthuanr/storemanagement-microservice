
import uvicorn
from fastapi import FastAPI
import aio_pika
from contextlib import asynccontextmanager

from app.api import order_router
from app.database.database import Base, engine  
from app.brokers.rabbitmq import get_channel, get_connection, get_exchange
from app.consumers.order_consumer import setup_order_consumer
from app.services.publisher_adapter import PublisherAdapter
from app.services.order_service import OrderService


from app.servicelogging.servicelogger import logger

# from app.brokers.rabbitmq import lifespan

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    connection = await get_connection()
    channel = await get_channel(connection)
    exchange = await get_exchange(channel)

    app.state.rabbitmq_exchange = exchange

    # ✅ Application-scoped instance OrderService
    publisher = PublisherAdapter(app)
    order_service = OrderService(publisher)
    app.state.order_service = order_service

    # Application-scoped instance
    publisher = PublisherAdapter(app)
    app.state.order_service = OrderService(publisher)

    # Register consumer
    await setup_order_consumer(channel, exchange, order_service)
    yield
    # Shutdown
    await connection.close()


app = FastAPI(title="Order Service",lifespan=lifespan)

# Đăng ký route
app.include_router(order_router.router)

# Tạo bảng DB
Base.metadata.create_all(bind=engine)

def main():
    logger.info("🚀 Starting FastAPI app...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
    
