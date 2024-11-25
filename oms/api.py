from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from oms.schemas import OrderRequest
from oms.crud import create_order, get_orders, get_order
from oms.database import get_db

router = APIRouter()

@router.post("/orders/")
async def create_order_route(order: OrderRequest, db: Session = Depends(get_db)):
    try:
        return await create_order(order, db)
    except HTTPException as e:
        raise e

@router.get("/orders/")
def read_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.get("/orders/{order_id}")
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
