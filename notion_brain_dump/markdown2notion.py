from md2notionpage.core import parse_md
import os
from notion_client import Client

# load_dotenv()
os.environ["NOTION_SECRET"] = "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"
notion = Client(auth=os.environ["NOTION_SECRET"])

markdown_text = """
Sure! Here's the entire explanation formatted properly in Markdown:

---

# 🧠 Using Notional to Convert Markdown or HTML to Notion Pages

**Notional** is a powerful and Pythonic SDK for the Notion API. While it doesn't natively convert Markdown or HTML, it integrates well with other tools that handle this parsing for you.

---

## 🧰 Recommended Tools for Markdown/HTML to Notion Conversion

| Package                                                    | Description                                                                                | Notes                                                                                 |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| [`md2notionpage`](https://pypi.org/project/md2notionpage/) | Converts Markdown text into Notion pages, handling inline formatting and block structures. | Simplifies the process of creating Notion pages from Markdown.                        |
| [`html2notion`](https://github.com/selfboot/html2notion)   | Transforms HTML content into Notion blocks, supporting various HTML tags.                  | Useful for importing HTML documents into Notion.                                      |
| [`md2notion`](https://pypi.org/project/md2notion/)         | Imports Markdown files into Notion, preserving formatting and structure.                   | Requires `notion-py`, which may have compatibility issues with the latest Notion API. |

---

## 🧑‍💻 Example: Using `md2notionpage` with Notional

### 1. Install Required Packages

```bash
pip install notional md2notionpage
```

### 2. Python Script

```python
import os
from notional import Notion
from md2notionpage import md2notionpage

# Initialize Notion client with your integration token
notion = Notion(auth=os.environ["NOTION_TOKEN"])

# Read Markdown content from a file
with open("example.md", "r", encoding="utf-8") as md_file:
    markdown_content = md_file.read()

# Convert Markdown to Notion blocks
notion_blocks = md2notionpage(markdown_content)

# Create a new page in your workspace
new_page = notion.pages.create(
    parent={"type": "page_id", "page_id": os.environ["NOTION_PARENT_PAGE_ID"]},
    properties={
        "title": [
            {
                "type": "text",
                "text": {"content": "Imported Markdown Page"}
            }
        ]
    },
    children=notion_blocks
)

print(f"Page created: {new_page['url']}")
```

> **Note:** Ensure that you set the following environment variables:
>
> * `NOTION_TOKEN`: your Notion integration token
> * `NOTION_PARENT_PAGE_ID`: the ID of the parent page or database

---

## 🔍 Summary

While **Notional** is excellent for interacting with the Notion API, combining it with tools like `md2notionpage` or `html2notion` enables seamless conversion of Markdown or HTML content into Notion pages.

These tools handle the parsing and block formatting for you, letting you focus on the actual content creation.

---

Would you like me to provide a full working GitHub Gist or a CLI tool based on this?

"""

title = "Markdown to Notion Page"

parent_page_id = "1ec84ade96ac803bbe86e258a017466b"

created_page = notion.pages.create(
    parent={"type": "page_id", "page_id": parent_page_id}, properties={}, children=[]
)

# notion_page_url = md2notionpage(markdown_text, title, parent_page_id)
notion.pages.update(
    created_page["id"],
    properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
)

# Iterate through the parsed Markdown blocks and append them to the created page
for block in parse_md(markdown_text):
    notion.blocks.children.append(created_page["id"], children=[block])
