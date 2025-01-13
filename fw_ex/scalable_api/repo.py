# pyright: reportMissingImports=false

from sqlalchemy.orm import Session
from models import User, Order


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, name: str):
        user = User(name=name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_orders(self, user_id: int):
        return self.db.query(Order).filter(Order.user_id == user_id).all()

    def create_order(self, user_id: int, item_name: str):
        order = Order(user_id=user_id, item_name=item_name)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
