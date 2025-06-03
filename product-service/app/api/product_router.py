from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas import product_schema as schema
from app.crud import product_crud as crud
# from app.services.inventory_client import get_inventory
from app.services.inventory_client import InventoryClient
import grpc


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/products/", response_model=schema.ProductOut)
def create_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/products/{product_id}/", response_model=schema.ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)

@router.get("/products/{product_id}/inventory")
def read_product_inventory(product_id: int):
    inventory_client = InventoryClient()
    try:
        inventory = inventory_client.get_inventory(product_id)
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory Not Found!!!")
        return inventory
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
