# inventory_crud.py

from sqlalchemy.orm import Session
from app.models.inventory import Inventory
import app.proto.inventory_pb2 as inventory_pb2


def get_inventory_by_id(db: Session, inventory_id: int):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if inventory:
        return inventory_pb2.InventoryResponse(
            id=inventory.id,
            name=inventory.name,
            description=inventory.description or "",
            price=float(inventory.price),
            stock=inventory.stock,
            created_at=str(inventory.created_at),
            updated_at=str(inventory.updated_at),
        )
    return None


def get_all_inventory(db: Session):
    inventories = db.query(Inventory).all()
    return inventory_pb2.InventoryListResponse(
        inventories=[
            inventory_pb2.InventoryResponse(
                id=item.id,
                name=item.name,
                description=item.description or "",
                price=float(item.price),
                stock=item.stock,
                created_at=str(item.created_at),
                updated_at=str(item.updated_at),
            )
            for item in inventories
        ]
    )


def create_inventory(db: Session, request: inventory_pb2.CreateInventoryRequest):
    new_item = Inventory(
        name=request.name,
        description=request.description,
        price=request.price,
        stock=request.stock,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return inventory_pb2.InventoryResponse(
        id=new_item.id,
        name=new_item.name,
        description=new_item.description,
        price=float(new_item.price),
        stock=new_item.stock,
        created_at=str(new_item.created_at),
        updated_at=str(new_item.updated_at),
    )


def update_inventory(db: Session, request: inventory_pb2.InventoryUpdateRequest):
    inventory = db.query(Inventory).filter(Inventory.id == request.id).first()
    if not inventory:
        return None
    inventory.name = request.name
    inventory.description = request.description
    inventory.price = request.price
    inventory.stock = request.stock
    db.commit()
    db.refresh(inventory)
    return inventory_pb2.InventoryResponse(
        id=inventory.id,
        name=inventory.name,
        description=inventory.description,
        price=float(inventory.price),
        stock=inventory.stock,
        created_at=str(inventory.created_at),
        updated_at=str(inventory.updated_at),
    )


def delete_inventory(db: Session, inventory_id: int):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        return inventory_pb2.DeleteInventoryResponse(success=False)
    db.delete(inventory)
    db.commit()
    return inventory_pb2.DeleteInventoryResponse(success=True)
