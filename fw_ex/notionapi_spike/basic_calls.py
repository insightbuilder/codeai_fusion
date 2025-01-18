import os
from notion_client import Client

# pyright: reportMissingImports=false


notion = Client(auth=os.environ["NOTION_TOKEN"])

users = notion.users.list()

for user in users.get("results"):
    name, user_type = user["name"], user["type"]
    print(f"{name} is a name")
    print(f"User type is a {user_type}")
