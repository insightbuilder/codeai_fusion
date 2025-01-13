# object creation is transferred to fw / container

# this is havin all the services as dict


from tightly_coupled import DatabaseService
from inject_deps import UserService


class IoCContainer:
    def __init__(self):
        self.services = {}

    def register(self, name, service):
        self.services[name] = service

    def resolve(self, key):
        return self.services[key]


ioc = IoCContainer()

ioc.register("db_service", DatabaseService())
ioc.register("user_service", UserService(ioc.resolve("db_service")))

user_service = ioc.resolve("user_service")
user_service.get_user()

# services are regd and resolved in central app
# works in framework
# better maintainability
