import os
import time
import logging
from notion_client import Client
from rich import print

# pyright: basic
# ruff: noqa
# pyright: reportMissingImports=false

# Configuration
NOTION_TOKEN = os.environ["YTDEMO_TOKEN"]

# Initialize clients
notion = Client(auth=NOTION_TOKEN)

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Track last updated blocks
last_updated = {}


def get_page_blocks(page_id):
    """Fetch all blocks of a given Notion page."""
    try:
        blocks = notion.blocks.children.list(block_id=page_id)
        return blocks.get("results", [])
    except Exception as e:
        logging.error(f"Error fetching blocks: {e}")
        return []


def fetch_text_blocks(blocks):
    """Extract and track updated text blocks from Notion."""
    text_blocks = []
    print(f"The blocks: {blocks}")
    for block in blocks:
        block_id = block["id"]
        last_edited_time = block["last_edited_time"]
        if block["type"] == "paragraph":
            logging.info(
                block["paragraph"]["rich_text"][0]["plain_text"]
            )  # Log the rich_text content of the block["paragraph"]["rich_text"]

            if (
                block_id not in last_updated
                or last_updated[block_id] != last_edited_time
            ):
                print(block["type"])
                text_blocks.append((
                    block_id,
                    block["paragraph"]["rich_text"][0]["plain_text"],
                ))
                last_updated[block_id] = last_edited_time  # Update tracker
            print("last_updated", last_updated)
    logging.info("Exiting for block")
    logging.info(f"text_blocks: {text_blocks}")
    return text_blocks


def update_notion_block(block_id, new_text):
    """Update Notion block with OpenAI-generated content."""
    try:
        notion.blocks.update(
            block_id=block_id,
            paragraph={"text": [{"type": "text", "text": {"content": new_text}}]},
        )
        logging.info(f"Updated block {block_id} with AI response")
    except Exception as e:
        logging.error(f"Error updating Notion block {block_id}: {e}")


if __name__ == "__main__":
    # list the users
    # list_users = notion.users.list()
    # print(list_users)

    # list everything that is shared
    search_result = notion.search().get("results")
    for data in search_result:
        print(data["object"])
        print(data["id"])
    # print(search_result)

    # list the blocks in the page
    blocks = notion.blocks.children.list(block_id="1aa5132d889c80f5af5df41dbe4a2514")
    print(blocks)

    # list the pages in the database
    pages = notion.databases.query(database_id="1aa5132d-889c-8098-b247-d2825423706e")
    print(pages)

    # adding a block to the page
    tobj = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"text": {"content": "This is a New Para by Python"}}]
        },
    }
    notion.blocks.children.append(
        block_id="1aa5132d889c80f5af5df41dbe4a2514", children=[tobj]
    )
    print("Adding block completed")
    # adding page into a database
    newpage = {
        "Name": {"title": [{"text": {"content": "Page Added by Python"}}]},
    }
    notion.pages.create(
        parent={"database_id": "1aa5132d-889c-8098-b247-d2825423706e"},
        properties=newpage,
    )
    print("Adding page completed")
