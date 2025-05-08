from md2notionpage.core import parse_md
import os
from notion_client import Client
from anthropic import Anthropic

# load_dotenv()
notion = Client(auth=os.environ["NOTION_TOKEN"])
anthropic = Anthropic()

while True:
    query = input("Enter a query: ")
    if query == "":
        print("Goodbye!")
        break
    messages = [{"role": "user", "content": query}]

    # Initial Claude API call
    response = anthropic.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        messages=messages,
    )

    markdown_text = response.content[0].text
    print(f"Markdown text: {markdown_text}")

    parent_page_id = "1ec84ade96ac803bbe86e258a017466b"

    created_page = notion.pages.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        properties={},
        children=[],
    )

    # notion_page_url = md2notionpage(markdown_text, title, parent_page_id)
    notion.pages.update(
        created_page["id"],
        properties={"title": {"title": [{"type": "text", "text": {"content": query}}]}},
    )

    # Iterate through the parsed Markdown blocks and append them to the created page
    for block in parse_md(markdown_text):
        notion.blocks.children.append(created_page["id"], children=[block])
