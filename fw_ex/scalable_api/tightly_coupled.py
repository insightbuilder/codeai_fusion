class DatabaseService:
    def connect(self):
        print("Connecting to database...")


class UserService:
    def __init__(self) -> None:
        self.db_service = DatabaseService()  # hard coded

    def get_user(self):
        self.db_service.connect()
        print("Getting user...")


if __name__ == "__main__":
    user_service = UserService()
    user_service.get_user()

# UserService creates DatabaseService directly, so its tightly coupled

# Difficult to test, deps cannot be mocked

# New Services adding can be a challenge, violating Open/Close principle
