
import sys
import os
BASE_DIR = os.path.dirname(__file__)
# Thêm thư mục 'proto/' vào sys.path
PROTO_DIR = os.path.join(BASE_DIR, "proto")
sys.path.append(PROTO_DIR)

from fastapi import FastAPI
from app.api.product_router import router as product_router
from app.database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product_router, prefix="/api")
