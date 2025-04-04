from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import List
from pywebio.input import input
from pywebio.output import put_markdown, put_text, put_grid, put_scope, put_tabs, use_scope, put_button, put_row, put_column, put_html
from pywebio.session import run_js
from functools import partial
import traceback
import os


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


data_writer_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="Write the given data to a file",
    result_type=str,
)


@data_writer_agent.tool
async def write_data(ctx: RunContext[dict], data: str, file_name: str) -> str:
    """Tool to write data to a file"""
    put_text(f"Adding data to {file_name}")
    put_text(f"Data is: {data}")
    # storing data in cache
    ctx.deps["file_name"] = file_name
    ctx.deps["video_titles"] = data
    try:
        # the write will append the data to the file
        # even if we ask to delete the lines, it will
        # be appended as new data.
        with open(file_name, "a+") as f:
            f.write("\n*** Writing Agent data ***\n")
            f.write(data)
        return "Data written to file"
    except Exception as e:
        return f"Error writing data to file: {e}"


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


# Add custom styling
put_html("""
<style>
.webio-tabs {
    height: 100vh;
    overflow: auto;
}
.file-explorer {
    border-left: 1px solid #ccc;
    padding-left: 1rem;
}
.file-content {
    border-top: 1px solid #ccc;
    margin-top: 1rem;
    padding-top: 1rem;
    max-height: 500px;
    overflow: auto;
}
</style>
""")


while True:
    # Create a two-column layout
    put_row([
        # Left column: Theme Builder
        put_column([
            put_markdown("### Welcome to Youtube Video Inspiration Builder Agent"),
            put_text("Enter your prompt:"),
        ], size='60%'),
        
        # Right column: File Explorer
        put_column([
            put_markdown("### File Explorer"),
            # File list
            put_column([
                put_text(f"Current directory: {os.getcwd()}"),
                *[put_button(file, onclick=partial(show_file_contents, file)) 
                  for file in os.listdir() 
                  if os.path.isfile(file)]
            ], size='40%'),
            # File content viewer
            put_markdown("### File Content"),
            put_scope('file_content')
        ], size='40%')
    ])

    your_prompt = input()  # Get input after layout is created
    
    if your_prompt == "" or your_prompt == "bye":
        break
    
    # Theme builder logic
    put_text(f"You: {your_prompt}")
    try:
        result = theme_building_agent.run_sync(your_prompt, deps=cache)
        put_text(type(result.data))
        put_text(f"Pydantic Agent:  {result.data}")
        put_text("Do you wish to store the title to file")
        # Each part of the agent is split into a if-else
        # block to complete a particular work.
        choice = input("y/n: ")
        if choice == "y":
            file_name = input("Enter the file name: ")
            write_result = data_writer_agent.run_sync(
                f"Write the {result.data} to {file_name}",
                deps=cache,
            )
            put_text(f"File Write: {write_result}")
        else:
            put_text("Titles not stored to file")

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
