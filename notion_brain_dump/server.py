from mcp.server.fastmcp import FastMCP
from notion_client import AsyncClient
import os
from typing import List

token = "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"
mcp = FastMCP("notion_bd_server")
brain = AsyncClient(auth=token)


@mcp.tool()
async def add_task(task: str):
    """Add a task to the Notion database and returns the new page ID"""
    dump_db = "1d784ade96ac80a3b7ecf54f3eae5f49"
    newpage = {
        "TaskTitle": {"title": [{"text": {"content": task}}]},
    }
    pg_create = await brain.pages.create(
        parent={"database_id": dump_db},
        properties=newpage,
    )
    return f"Task has been added {pg_create['id']}"


@mcp.resource("notion://dumpdb/all")
async def get_all_database_items():
    dump_db = "1d784ade96ac80a3b7ecf54f3eae5f49"
    all_results = []
    next_cursor = None

    while True:
        response = (
            await brain.databases.query(database_id=dump_db, start_cursor=next_cursor)
            if next_cursor
            else await brain.databases.query(database_id=dump_db)
        )

        all_results.extend(response["results"])

        if response.get("has_more"):
            next_cursor = response["next_cursor"]
        else:
            break

    text_conv = ""
    for result in all_results:
        page_id = result["id"]
        last_edited_time = result["last_edited_time"]
        # getting the properties now
        task_title = result["properties"]["TaskTitle"]["title"][0]["text"]["content"]
        task_status = result["properties"]["TaskStatus"]["select"]
        area = result["properties"]["Area"]["rich_text"]
        resource = result["properties"]["Resource"]["rich_text"]
        due_date = result["properties"]["DueDate"]["date"]
        url = result["url"]
        text_conv += f"Task: {task_title}\t Status: {task_status}\t Area: {area}\t Resource: {resource}\t Due Date: {due_date}\t URL: {url}\t Page ID: {page_id}\t  Last Edited Time: {last_edited_time}\t "
    # return results[0]["text"]
    return text_conv


@mcp.tool()
async def list_task():
    """Lists the tasks in the Notion database as text"""
    tlist = await mcp.read_resource("notion://dumpdb/all")
    return tlist


@mcp.tool()
async def remove_task(task_text: str):
    """Search for the task from the Notion database and delete it"""
    dump_db = "1d784ade96ac80a3b7ecf54f3eae5f49"
    search_results = await brain.databases.query(
        database_id=dump_db,
        filter={
            "property": "TaskTitle",
            "title": {
                "equals": task_text,
            },
        },
    )
    results = search_results.get("results", [])
    page_id = results[0]["id"]
    delete_page = await brain.pages.update(page_id=page_id, archived=True)
    return delete_page


@mcp.tool()
async def add_resource(task_text: str, resource_text: str):
    """Search for the task from the Notion database and add resource to it"""

    dump_db = "1d784ade96ac80a3b7ecf54f3eae5f49"

    search_results = await brain.databases.query(
        database_id=dump_db,
        filter={
            "property": "TaskTitle",
            "title": {
                "equals": task_text,
            },
        },
    )
    results = search_results.get("results", [])

    page_id = results[0]["id"]
    prop = {}

    prop["Resource"] = {
        "type": "rich_text",
        "rich_text": [{"text": {"content": resource_text}}],
    }

    updt = await brain.pages.update(page_id=page_id, properties=prop)
    return f"Updated the resource to {updt['id']}"


@mcp.tool()
async def add_area(task_text: str, area_text: str):
    """Search for the task from the Notion database and add area to it"""

    dump_db = "1d784ade96ac80a3b7ecf54f3eae5f49"

    search_results = await brain.databases.query(
        database_id=dump_db,
        filter={
            "property": "TaskTitle",
            "title": {
                "equals": task_text,
            },
        },
    )
    results = search_results.get("results", [])

    page_id = results[0]["id"]
    prop = {}

    if area_text:
        prop["Area"] = {
            "type": "rich_text",
            "rich_text": [{"text": {"content": area_text}}],
        }

    updt = await brain.pages.update(page_id=page_id, properties=prop)
    return f"Updated the area to {updt['id']}"


@mcp.prompt()
def task_steps(task_text: str) -> str:
    """Prompt to get the steps to complete the tasks"""
    return f"Provide the step by approach required to complete the {task_text}"


@mcp.prompt()
def task_analysis(tasks: str) -> str:
    """Prompt to analyse the tasks"""
    return f"Analyse the {tasks} and provide the steps to complete the task"


@mcp.resource("notion://dumpdb/{task_text}")
async def search_db(task_text: str) -> str:
    """Get the filtered task from the Notion database and returns the data as text"""
    dump_db = "1d784ade96ac80a3b7ecf54f3eae5f49"
    search_results = await brain.databases.query(
        database_id=dump_db,
        filter={
            "property": "TaskTitle",
            "title": {
                "contains": task_text,
            },
        },
    )
    results = search_results.get("results", [])
    text_conv = ""
    for result in results:
        page_id = result["id"]
        created_time = result["created_time"]
        last_edited_time = result["last_edited_time"]
        # getting the properties now
        task_title = result["properties"]["TaskTitle"]["title"][0]["text"]["content"]
        task_status = result["properties"]["TaskStatus"]["select"]
        area = result["properties"]["Area"]["rich_text"]
        resource = result["properties"]["Resource"]["rich_text"]
        due_date = result["properties"]["DueDate"]["date"]
        url = result["url"]
        text_conv += f"Task: {task_title}\t Status: {task_status}\t Area: {area}\t Resource: {resource}\t Due Date: {due_date}\t URL: {url}\t Page ID: {page_id}\t  Last Edited Time: {last_edited_time}\t "
    # return results[0]["text"]
    return text_conv


# @mcp.tool()
async def analyse_tasks(task_kw: str) -> str:
    """Searches the database for the task, and gets the steps to complete the task"""
    task_info = await mcp.read_resource(f"notion://dumpdb/{task_kw}")
    assembled_prompt = await mcp.get_prompt(
        "task_analysis",
        arguments={
            "tasks": task_info[0].content,
        },
    )
    return assembled_prompt.messages[0].content.text


@mcp.tool()
async def update_task(task_title: str, task_data: str):
    """Update the task in the database with given task title"""
    # First find the task and get its page id
    dump_db = "1d784ade96ac80a3b7ecf54f3eae5f49"

    search_results = await brain.databases.query(
        database_id=dump_db,
        filter={
            "property": "TaskTitle",
            "title": {
                "equals": task_title,
            },
        },
    )
    results = search_results.get("results", [])
    page_id = results[0]["id"]

    # Then update the data into the page using append method
    page_data = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"text": {"content": task_data}}]},
    }

    await brain.blocks.children.append(
        block_id=page_id,
        children=[page_data],
    )
    # Inform the LLM that the work has been done
    return f"The page with {page_id} has been updated"


# "TaskTitle": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "test", "link": null}, "annotations": {"bold": false, "italic": false, "strikethrough": false, "underline": false, "code": false, "color": "default"}, "plain_text": "test", "href": null}] [ "properties": {"TaskStatus": {"id": "IJax", "type": "select", "select": null}, "Area": {"id": "c%3C%60%7C", "type": "rich_text", "rich_text": []}, "DueDate": {"id": "ce%3DU", "type": "date", "date": null}, "Resource": {"id": "kUxZ", "type": "rich_text", "rich_text": []}, }}, "url": "https://www.notion.so/test-1d784ade96ac81a38f7bdd1eccaa13c4", "public_url": null}]',]
if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
