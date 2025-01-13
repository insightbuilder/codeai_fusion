class DatabaseService:
    def connect(self):
        print("Connecting to database...")


class UserService:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    def get_user(self):
        self.db_service.connect()
        print("Getting user...")


if __name__ == "__main__":
    db_service = DatabaseService()

    usersvc = UserService(db_service)
    usersvc.get_user()

# services just recieve dependencies, don't create
# testing is easy with mocking
# Implementation can be swapped
