from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from core.database import Base
from repositories.user_repository import User  # Assuming you have a User model


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"), index=True)
    item = Column(String)

    user = relationship("User", back_populates="orders")


def create_order(db: Session, username: str, item: str):
    """
    Creates a new order for the authenticated user.
    """
    new_order = Order(username=username, item=item)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_orders(db: Session, username: str):
    """
    Retrieves all orders for the authenticated user.
    """
    orders = db.query(Order).filter(Order.username == username).all()
    return orders
