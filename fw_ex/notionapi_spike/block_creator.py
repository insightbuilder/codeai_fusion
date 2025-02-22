from pywebio.input import input, os
from pywebio.output import (
    put_table,
    put_text,
    put_buttons,
    put_success,
    put_error,
    put_button,
)
from pywebio.platform import start_server
from pywebio.session import hold
from notion_client import Client

# pyright: reportArgumentType=false
# Initialize Notion Client
notion = Client(auth=os.environ["NOTION_TOKEN"])

# Store Notion Page ID in memory (simulated state)
PAGE_ID = None


def insert_object(object_type):
    """Inserts selected object type into Notion page"""
    global PAGE_ID
    if not PAGE_ID:
        put_error("No Page ID set! Enter a valid Page ID first.")
        return

    # Define object types
    block_types = {
        "Heading": {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"text": {"content": "New Heading"}}],
            },
        },
        "Paragraph": {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "text": {"content": "This is a paragraph."},
                    }
                ],
            },
        },
        "Bullet List": {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": "Bullet item"}}],
            },
        },
        "Numbered List": {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"text": {"content": "Numbered item"}}],
            },
        },
        "Quote": {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": [{"text": {"content": "Inspirational Quote"}}],
            },
        },
        "To-do": {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [
                    {
                        "text": {"content": "Task item"},
                    }
                ],
            },
        },
        "Divider": {"object": "block", "type": "divider", "divider": {}},
        "Code Block": {
            "object": "block",
            "type": "code",
            "code": {
                "caption": [],
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "print('Hello World')"},
                    }
                ],
                "language": "python",
            },
        },
        "Callout": {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"text": {"content": "Important Note"}}],
            },
        },
        "Toggle List": {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"text": {"content": "Click to expand"}}],
            },
        },
    }

    try:
        put_text(f"Inserting {object_type}...")
        put_text(block_types[object_type])
        # Insert block into the Notion page
        notion.blocks.children.append(
            block_id=PAGE_ID, children=[block_types[object_type]]
        )
        put_success(f"{object_type} inserted successfully!")
    except Exception as e:
        put_error(f"Failed to insert {object_type}: {str(e)}")


def create_para():
    """Creates a new block inside the specified Notion page."""
    notion.blocks.children.append(
        block_id=PAGE_ID,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "This is a New Para"}}]
                },
            }
        ],
    )
    put_success(f"Added new block to page {PAGE_ID}.")


def get_shared_pages_and_databases():
    """
    Fetch all pages and databases that are shared with the current Notion integration.
    """
    response = notion.search()
    shared_items = []

    for item in response["results"]:
        item_type = item["object"]
        item_url = item.get("url")
        # print(item_url)
        if item_type == "page":
            # item_title = item_url.split("-")[-2]
            shared_items.append([item["id"], item_type, item_url, "Ref Page URL"])
        else:
            shared_items.append([
                item["id"],
                item_type,
                item_url,
                item.get("title")[0]["plain_text"],
            ])
        # break

    put_table([["ID", "Type", "URL", "Title"]] + shared_items)


def main():
    """Main PyWebIO interface"""
    put_button("Shared Items", get_shared_pages_and_databases)

    global PAGE_ID
    PAGE_ID = input("Enter Notion Page ID:", type="text")

    put_text(f"Using Page ID: {PAGE_ID}")
    put_text("Select an object to insert:")

    # put_button("Create Paragraph", create_para)

    put_buttons(
        [
            "Heading",
            "Paragraph",
            "Bullet List",
            "Numbered List",
            "Quote",
            "To-do",
            "Divider",
            "Code Block",
            "Callout",
            "Toggle List",
        ],
        onclick=insert_object,
    )

    # hold()  # Keep the server running


if __name__ == "__main__":
    start_server(main, port=8080)
