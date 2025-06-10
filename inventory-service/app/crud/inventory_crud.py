# app/crud/inventory_crud.py

from sqlalchemy.orm import Session
from app.models.inventory import Inventory


def get_inventory_by_id(db: Session, inventory_id: int) -> Inventory | None:
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()


def get_all_inventory(db: Session) -> list[Inventory]:
    return db.query(Inventory).all()


def create_inventory(db: Session, name: str, description: str, price: float, stock: int) -> Inventory:
    new_item = Inventory(name=name, description=description, price=price, stock=stock)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update_inventory(db: Session, inventory_id: int, **fields) -> Inventory | None:
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        return None
    for key, value in fields.items():
        setattr(inventory, key, value)
    db.commit()
    db.refresh(inventory)
    return inventory


def delete_inventory(db: Session, inventory_id: int) -> bool:
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        return False
    db.delete(inventory)
    db.commit()
    return True
