import os
import time
import logging
from notion_client import Client
from openai import OpenAI
from rich import print

# pyright: basic
# ruff: noqa
# pyright: reportMissingImports=false

# Configuration
NOTION_TOKEN = os.environ["YTDEMO_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PAGE_ID = "1965132d-889c-802a-b597-f3395ebbbfc8"  # Notion Page ID to monitor

# Initialize clients
notion = Client(auth=NOTION_TOKEN)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

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
    # logging.info("Blocks entering Fetch blocks", blocks)
    # {'object': 'block', 'id
    # ': '1a35132d-889c-8074-b809-f48039f29007', 'parent': {'type': 'page_id', 'page_id': '1965132d-889c-802a-b597-f3395ebbbfc8'}, 'created_time
    # ': '2025-02-23T01:45:00.000Z', 'last_edited_time': '2025-02-23T01:46:00.000Z', 'created_by': {'object': 'user', 'id': 'c4ec5bcb-19e7-43d7-
    # a7c9-1de94c73f984'}, 'last_edited_by': {'object': 'user', 'id': 'c4ec5bcb-19e7-43d7-a7c9-1de94c73f984'}, 'has_children': False, 'archived'
    # : False, 'in_trash': False, 'type': 'paragraph', 'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': 'This is weird why no up
    # date', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color':
    # 'default'}, 'plain_text': 'This is weird why no update', 'href': None}], 'color': 'default'}},
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


def get_openai_inference(text):
    """Send text to OpenAI and return formatted response."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error from OpenAI: {e}")
        return None


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


def monitor_notion_page():
    """Monitor the Notion page for updates and apply AI responses."""
    logging.info("Monitoring Notion page for updates...")

    while True:
        try:
            blocks = get_page_blocks(PAGE_ID)
            logging.info("Blocks updates in monitoring:")
            text_blocks = fetch_text_blocks(blocks)
            print("Text blocks updates in monitoring:", text_blocks)
            if not text_blocks:
                logging.info("No new updates found. Waiting...")
            # else:
            #     for block_id, text in text_blocks:
            #         logging.info(
            #             f"Processing Block: {block_id} -> {text[:50]}..."
            #         )  # Preview text
            #         # ai_response = get_openai_inference(text)

            #         # if ai_response:
            #         #     update_notion_block(block_id, ai_response)

        except Exception as e:
            logging.error(f"Unexpected error in monitoring loop: {e}")

        time.sleep(10)  # Poll every 10 seconds (adjust as needed)


if __name__ == "__main__":
    monitor_notion_page()
