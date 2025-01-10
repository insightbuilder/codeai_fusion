from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import List
from pywebio.input import input
from pywebio.output import put_markdown, put_text, put_grid, put_scope, put_tabs, use_scope, put_button, put_row, put_column, put_html
from pywebio.session import run_js
from functools import partial
import traceback
import os
import asyncio


# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false


class YoutubeTitles(BaseModel):
    titles: List[str]


theme_building_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt=(
        "You are youtube video theme building agent."
        "Use only the get_titles tool to generate titles on the given topic"
        "Choose two of te best titles and return them"
        "To find why to create a video you should use only the get_why_reason tool"
        "Choose only one best tool for each activity"
    ),
    result_type=str,
)

title_generation_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="Generate youtube 5 titles on the given topic",
    result_type=YoutubeTitles,
)


@theme_building_agent.tool
async def get_titles(ctx: RunContext[dict], topic: str) -> YoutubeTitles:
    """Tool to generate 5 titles using the title generation agent"""
    put_text("Entering Tool: get_titles with topic", topic)
    # adding topic to cache
    ctx.deps["topic"] = topic
    titles = await title_generation_agent.run(
        f"Generate 5 titles on Youtube video title on {topic}"
    )
    return titles.data


why_video_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="List down 5 reasons to create a video on given topic",
    result_type=str,
)


@theme_building_agent.tool
async def get_why_reason(ctx: RunContext[dict], topic: str) -> str:
    """Tool to generate 5 reasons to create a video"""
    put_text(f"Entering Tool: get_why_reason with topic {topic}")
    reasons = await why_video_agent.run(
        f"List down 5 reasons to create a video on {topic}"
    )
    return reasons.data


cache = {}  # to store stuff that happens in agents


def show_file_contents(file_path: str) -> None:
    """Display contents of a file in the UI"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        with use_scope('file_content', clear=True):
            put_markdown(f"### File: {file_path}")
            put_text(content)
    except Exception as e:
        with use_scope('file_content', clear=True):
            put_text(f"Error reading file: {e}")

def write_to_file(data: str, file_name: str) -> str:
    """Simple function to write data to a file"""
    try:
        with open(file_name, "a+") as f:
            f.write("\n*** Writing data ***\n")
            f.write(data)
        return "Data written to file successfully"
    except Exception as e:
        return f"Error writing data to file: {e}"

def handle_store_result(data):
    """Simple synchronous handler for storing results"""
    file_name = input("Enter the file name: ")
    result = write_to_file(data, file_name)
    put_text(f"File Write: {result}")

def read_from_file(file_name: str) -> str:
    """Simple function to read data from a file and store in cache"""
    try:
        with open(file_name, "r") as f:
            content = f.read()
        # Store in cache with file name as key
        cache[file_name] = content
        return "Data read successfully and stored in cache"
    except Exception as e:
        return f"Error reading file: {e}"

def handle_read_result():
    """Handler for reading file contents"""
    file_name = input("Enter the file name to read: ")
    result = read_from_file(file_name)
    put_text(f"File Read: {result}")
    if file_name in cache:
        put_text("Cached content:")
        put_text(cache[file_name])

while True:

    your_prompt = input("Enter your request: ")  # Get input after layout is created
    
    if your_prompt == "" or your_prompt == "bye":
        break
    
    # Theme builder logic
    put_text(f"You: {your_prompt}")
    put_button("Read File", onclick=handle_read_result)
    try:
        result = theme_building_agent.run_sync(your_prompt, deps=cache)
        # put_text(type(result.data))
        put_text(f"Pydantic Agent:  {result.data}")
        
        # Replace the input prompt with buttons
        put_row([
            put_button("Store Result", onclick=partial(handle_store_result, result.data)),
            put_button("Skip", onclick=lambda: put_text("Skipped storing result"))
        ])

        # Continue with video theme building prompt
        put_text("Do you wish to continue video theme building?")
        choice = input("y/n: ")
        if choice == "y":
            if "topic" in cache:
                topic = cache["topic"]
            else:
                topic = input("Enter the topic again: ")
            why_result = theme_building_agent.run_sync(
                f"Why I should create the video on {topic}", deps=cache
            )
            put_text(f"Why create: {why_result.data}")
        else:
            put_text("Well what else you want to try???")

    except Exception as e:
        print(e)
        put_text(traceback.format_exc())
