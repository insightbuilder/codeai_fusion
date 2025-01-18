import os
import notion_client
from rich import print

# pyright: reportMissingImports=false

token = os.getenv("NOTION_TOKEN")
client = notion_client.Client(auth=token)

results = client.search().get("results")
print(len(results))
result = results[4]
# print(f"The result is a: {result['object']}")
print(f"The result is a: {result['properties']}")

prop_to_work = []

for key, prop in result["properties"].items():
    if "formula" not in prop.keys():
        if "select" in prop.keys():
            del prop["select"]
            prop_to_work.append({key: prop})
        elif "multi_select" in prop.keys():
            del prop["multi_select"]
            prop_to_work.append({key: prop})
        else:
            prop_to_work.append({key: prop})

print("Properties to work on: \n", prop_to_work)
