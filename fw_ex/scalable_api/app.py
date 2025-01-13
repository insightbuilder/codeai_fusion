from fastapi import FastAPI, Depends
from typing import Annotated
from db import get_db, Base, engine
from repo import UserRepository, OrderRepository
from services import UserService, OrderService
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_user_service(db: Session = Depends(get_db)):
    return UserService(UserRepository(db))


def get_order_service(
    db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)
):
    return OrderService(OrderRepository(db), user_service)


@app.post("/users")
def create_user(
    name: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return user_service.create_user(name)


@app.get("/users/{user_id}")
def get_user(
    user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return user_service.get_user(user_id)


@app.post("/orders")
def create_order(
    user_id: int,
    item_name: str,
    order_service: Annotated[OrderService, Depends(get_order_service)],
):
    return order_service.create_order(user_id, item_name)


@app.get("/orders/{user_id}")
def get_orders(
    user_id: int, order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return order_service.get_orders(user_id)
