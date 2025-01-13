from repositories.order_repository import create_order, get_orders

# from repositories.user_repository import get_user_by_username
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends


def place_order(
    db: Session,
    username: str,
    item: str,
    # current_user: dict = Depends(get_user_by_username),
):
    """
    Places a new order for the authenticated user.
    """
    # if not current_user["username"] != username:
    #     raise HTTPException(status_code=401, detail="Authentication required")
    print("Entering created  order service")
    return create_order(db, username, item)


def fetch_orders(db: Session):
    """
    Fetches all orders for the authenticated user.
    """
    # if not current_user["username"] != username:
    #     raise HTTPException(status_code=401, detail="Authentication required")

    return get_orders(db)
