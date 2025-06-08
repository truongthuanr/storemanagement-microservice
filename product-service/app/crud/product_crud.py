from sqlalchemy.orm import Session
from app import models
from app.schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    db_product = models.product.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.product.Product).filter(models.product.Product.id == product_id).first()

def get_all_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.product.Product).offset(skip).limit(limit).all()
