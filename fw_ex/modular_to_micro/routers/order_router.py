from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.auth import get_current_user
from services.order_service import place_order, fetch_orders
from pydantic import BaseModel
from typing import List

router = APIRouter()


class OrderRequest(BaseModel):
    item: str


class OrderResponse(BaseModel):
    order_id: int
    user: str
    item: str


@router.post("/", response_model=OrderResponse)
def place_order_route(
    order: OrderRequest,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    order_data = place_order(db, user, order.item)
    return OrderResponse(order_id=order_data.id, user=user, item=order.item)


@router.get("/", response_model=List[OrderResponse])
def list_orders_route(
    db: Session = Depends(get_db), user: str = Depends(get_current_user)
):
    orders = fetch_orders(db, user)
    return [OrderResponse(order_id=o.id, user=o.user, item=o.item) for o in orders]
