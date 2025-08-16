from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database.database import get_db
from app.crud import order_crud
from app.schemas.order_schema import (
    OrderCreate, OrderRead, OrderStatusUpdate, OrderStatusEnum
)
from app.exceptions.order_exception import OrderValidationError, ProductUnavailable
# from app.services.order_service import create_order_service
from app.servicelogging.servicelogger import logger
from app.services.publisher_adapter import PublisherAdapter
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

def get_order_service(request: Request) -> OrderService:
    return request.app.state.order_service   # instance global

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_crud.create_order(db, order)


@router.get("/", response_model=List[OrderRead])
def get_all_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return order_crud.get_all_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(order_id: int, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = order_crud.update_order_status(db, order_id, status_update.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = order_crud.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return

@router.post("/create_order", status_code=201)
async def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    service: OrderService = Depends(get_order_service)
):
    logger.info(f"Received create_order request from customer_id={payload.customer_id} with items={payload.items}")

    try:
        result = await service.create_order(db, payload)
        logger.info(f"Successfully created order: {result}")
        return result

    except (OrderValidationError, ProductUnavailable) as e:
        logger.warning(f"Business error: {str(e)}")
        raise HTTPException(status_code=400 if isinstance(e, OrderValidationError) else 502, detail=str(e))

    except Exception as e:
        logger.exception("Unexpected error while creating order")
        raise HTTPException(status_code=500, detail="Internal server error")
