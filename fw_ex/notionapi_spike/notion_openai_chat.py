import os
from notion_client import Client
from openai import OpenAI
from pywebio.input import input
from pywebio.output import (
    put_button,
    put_error,
    put_html,
    put_markdown,
    put_text,
    put_success,
)
from pywebio import start_server

# pyright: basic
# ruff: noqa
# pyright: reportMissingImports=false
# pyright: reportArgumentType=false

# Configuration
NOTION_TOKEN = os.environ["YTDEMO_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PAGE_ID = "1965132d-889c-802a-b597-f3395ebbbfc8"  # Notion Page ID to monitor

# Initialize clients
notion = Client(auth=NOTION_TOKEN)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def create_para_in_page(page_id, content):
    """Creates a new para block inside the specified Notion page."""
    try:
        notion.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"text": {"content": content}}]},
                }
            ],
        )
        put_success(f"Added new block to page {page_id}.")
    except Exception as e:
        put_error(f"Error in Creating Block: {e}")


def create_h2_in_page(page_id, content):
    """Creates a new heading 2 block inside the specified Notion page."""
    try:
        notion.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"text": {"content": content}}]},
                }
            ],
        )
        put_success(f"Added new heading to page {page_id}.")
    except Exception as e:
        put_error(f"Error in Creating Block: {e}")


def create_code_in_page(page_id, content):
    """Creates a new heading 2 block inside the specified Notion page."""
    try:
        notion.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "caption": [],
                        "rich_text": [{"text": {"content": content}}],
                        "language": "markdown",
                    },
                }
            ],
        )
        put_success(f"Added new text block to page {page_id}.")
    except Exception as e:
        put_error(f"Error in Creating Block: {e}")


def get_openai_inference(text, history=[]):
    """Send text to OpenAI and return formatted response."""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        # append history if supplied
        if len(history) > 0:
            messages.extend(history)

        # append the user request
        messages.append({"role": "user", "content": text})
        print("Before sent to OpenAI: ", messages)
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        put_error(f"Error from OpenAI: {e}")
        return None


def delete_page_children():
    children = notion.blocks.children.list(block_id=PAGE_ID)["results"]

    for child in children:
        notion.blocks.update(block_id=child["id"], archived=True)


def main():
    put_html("<h1>Welcome to OpenAI Notion Interface</h1>")
    past_memory = []
    while True:
        put_button("Clear Page", delete_page_children)
        user_input = input("Enter your query: ")
        # adding user input to past_memory
        put_text("Sending Input to Notion page")
        create_h2_in_page(page_id=PAGE_ID, content=user_input)
        put_text("Getting ChatGPT to respond")
        put_text(f"Past history content: {len(past_memory)}")
        model_out = get_openai_inference(text=user_input, history=past_memory)
        put_markdown(model_out)
        put_text("Sending model output to Notion Page")
        create_code_in_page(page_id=PAGE_ID, content=model_out)
        past_memory.append({"role": "user", "content": user_input})
        past_memory.append({"role": "assistant", "content": model_out})


if __name__ == "__main__":
    start_server(main, 8081)
