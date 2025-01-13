from gitFolders.codeai_fusion.fw_ex.scalable_api.ioc_shift_resp import IoCContainer


class Database:
    def connect(self):
        print("Connecting to database...")

    def disconnect(self):
        print("Disconnecting from database...")


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def fetch_user(self):
        self.db.connect()
        print("Getting user...")


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repository = user_repo

    def get_user(self):
        self.user_repository.fetch_user()


ioc = IoCContainer()

ioc.register("db_service", Database())
ioc.register(
    "user_repo",
    UserRepository(ioc.resolve("db_service")),
)
ioc.register("user_service", UserService(ioc.resolve("user_repo")))

user_service = ioc.resolve("user_service")
user_service.get_user()

# clear responsibility with different layers,
# methods interact with each other
# easy reusability
