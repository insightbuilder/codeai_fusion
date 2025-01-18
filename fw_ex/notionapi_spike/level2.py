import os
from rich import print
from notion_client import Client

# pyright: reportMissingImports=false

token = os.getenv("NOTION_TOKEN")
client = Client(auth=token)
# results = client.users.list().get("results")
results = client.search().get("results")
print(len(results))
for data in results:
    print(data["object"])
    print(data["id"])
print(results[4])
result = results[4]
print(f"The result is a: {result['object']}")
print(f"The result properties are : {result['properties']}")
print(f"The result title are : {result['title'][0]['text']['content']}")
db_id = result["id"]
# https://www.notion.so/insighthacker/python-sdk-db-17f84ade96ac80d7a240f2d22c2a26a1?pvs=4
page_name = input("Enter any Name:")

git_link = input("Enter github profile Name: ")

newpage = {
    "Name": {"title": [{"text": {"content": page_name}}]},
    "github-name": {
        "type": "rich_text",
        "rich_text": [{"type": "text", "text": {"content": git_link}}],
    },
    "language": {"type": "multi_select", "multi_select": [{"name": "python"}]},
}

client.pages.create(
    parent={"database_id": db_id},
    properties=newpage,
)
