from notion_client import Client
import os
from md2notion.upload import convert

client = Client(auth=os.environ["NOTION_TOKEN"])

with open("test_markdown.md", "r", encoding="utf-8") as mdFile:
    rendered = convert(mdFile)
    print(rendered)
