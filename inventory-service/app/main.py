from fastapi import FastAPI
from .api.product_router import router as product_router
from .database import engine, Base

app = FastAPI(title="Inventory Service")

# Khởi tạo database nếu chưa có
Base.metadata.create_all(bind=engine)

# Đăng ký router
app.include_router(product_router, prefix="/products", tags=["Products"])

@app.get("/")
def root():
    return {"message": "Inventory Service is running"}
