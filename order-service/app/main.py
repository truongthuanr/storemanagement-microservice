import os
import threading
import uvicorn
from fastapi import FastAPI
from app.api import order_router
# from app.consumers.inventory_consumer import start_inventory_response_consumer 

app = FastAPI(title="Order Service")

# Include routers
app.include_router(order_router.router)


# Optional: Run consumer in background thread (nếu bạn muốn xử lý phản hồi từ inventory)
# def run_consumer():
#     start_inventory_response_consumer()


def main():
    # Optional: start consumer thread
    # consumer_thread = threading.Thread(target=run_consumer, daemon=True)
    # consumer_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
    
