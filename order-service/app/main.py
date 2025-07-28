
import uvicorn
from fastapi import FastAPI
from app.api import order_router
from app.database.database import Base, engine  
from contextlib import asynccontextmanager
import aio_pika
from app.servicelogging.servicelogger import logger

from app.brokers.rabbitmq import lifespan

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
    
