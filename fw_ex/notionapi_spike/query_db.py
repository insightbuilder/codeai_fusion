import os
import notion_client
from rich import print

# pyright: reportMissingImports=false

token = os.getenv("NOTION_TOKEN")
client = notion_client.Client(auth=token)

results = client.search().get("results")
print(len(results))
result = results[1]
print(f"The result is a: {result['object']}")
print(f"The result is a: {result['properties']}")
db_id = result["id"]

given_name = input("Enter name of the person you are looking for: ")

results = client.databases.query(**{
    "database_id": db_id,
    "filter": {"property": "Name", "title": {"equals": given_name}},
}).get("results")

print(len(results))

print(results)
