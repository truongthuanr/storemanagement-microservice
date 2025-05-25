from fastapi import FastAPI
from app.api.product_router import router as product_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product_router, prefix="/api")
