# app/crud/inventory_crud.py

from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.servicelogging.servicelogger import logger
from sqlalchemy import func

def get_inventory_by_id(db: Session, inventory_id: int) -> Inventory | None:
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()

# def get_stock_by_productid(db: Session, product_id: int) -> int | None:
#     logger.info("Function Start!")
#     result = db.query(func.sum(Inventory.stock)) \
#                 .filter(Inventory.product_id == product_id) \
#                 .scalar()
#     logger.info(f"Total stock for product_id={product_id} is {type(result)}:{result}")
#     return int(result or 0)

def get_stock_by_productid(db: Session, product_id: int) -> int | None:
    logger.info(f"Checking stock for product_id={product_id}")
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()

    if not inv:
        logger.info(f"No inventory found for product_id={product_id}")
        return None

    logger.info(f"Stock for product_id={product_id}: {inv.stock}")
    return inv.stock

def get_all_inventory(db: Session) -> list[Inventory]:
    return db.query(Inventory).all()


def create_inventory(
    db: Session,
    product_id: int,
    name: str,
    description: str,
    price: float,
    stock: int
) -> Inventory:
    logger.info("Function start!")
    new_item = Inventory(
        product_id=product_id,
        name=name,
        description=description,
        price=price,
        stock=stock
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    logger.info(
        f"Return | {new_item}"
        # f"product_id={product_id}, name={name}, price={price}, stock={stock}, id={new_item['id']}, \
        #     description={description}"
    )
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
