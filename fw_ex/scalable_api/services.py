# pyright: reportMissingImports=false

from repo import UserRepository, OrderRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int):
        return self.user_repo.get_user(user_id)

    def create_user(self, name: str):
        return self.user_repo.create_user(name)


class OrderService:
    def __init__(self, order_repo: OrderRepository, user_service: UserService):
        self.order_repo = order_repo
        self.user_service = user_service

    def get_orders(self, user_id: int):
        return self.order_repo.get_orders(user_id)

    def create_order(self, user_id: int, item_name: str):
        return self.order_repo.create_order(user_id, item_name)
