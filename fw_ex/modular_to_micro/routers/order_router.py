from fastapi import APIRouter, Depends
from routers.user_router import UserRequest
from sqlalchemy.orm import Session
from core.database import get_db

# from core.auth import get_current_user
from services.order_service import place_order, fetch_orders
from pydantic import BaseModel
from typing import List

# pyright: reportAttributeAccessIssue=false
# pyright: reportMissingImports=false

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
    user_req: UserRequest,
    db: Session = Depends(get_db),
    # user: str = Depends(get_current_user),
):
    order_data = place_order(db, user_req.username, order.item)
    return OrderResponse(
        order_id=order_data.id, user=user_req.username, item=order.item
    )


@router.get("/", response_model=List[OrderResponse])
def list_orders_route(
    # user_req: UserRequest,
    db: Session = Depends(get_db),
):
    orders = fetch_orders(db)
    return [OrderResponse(order_id=o.id, user=o.username, item=o.item) for o in orders]
