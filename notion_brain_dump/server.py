from mcp.server.fastmcp import FastMCP
from notion_client import AsyncClient
import os

token = "ntn_token"
mcp = FastMCP("notion_bd_server")
brain = AsyncClient(auth=token)

# The server has tools for doing CRUD operations on the Brain Dump database


@mcp.tool()
async def add_task(task: str):
    """Add a task to the Notion database and return the new page ID"""
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


@mcp.resource("notion://dumpdb/{task_text}")
async def search_db(task_text: str) -> str:
    """Get the filtered task from the Notion database and returns the data as text"""
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
async def change_title(task_title: str, new_title: str):
    """Change title of the task"""

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
    prop = {}

    prop["TaskTitle"] = {
        "type": "title",
        "title": [{"text": {"content": new_title}}],
    }

    updt = await brain.pages.update(page_id=page_id, properties=prop)
    return f"Updated the title of the page {updt['id']}"


@mcp.tool()
async def add_page_content(task_title: str, task_data: str):
    """Append the task data into the page of given task title"""
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
    return f"The content has been added to {page_id}"


@mcp.tool()
async def read_page_content(task_title: str):
    """Append the task data into the page of given task title"""
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
    # getting the page blocks
    page_blocks = await brain.blocks.children.list(block_id=page_id)
    page_text = ""
    for block in page_blocks["results"]:
        page_text += block["paragraph"]["rich_text"][0]["text"]["content"]
    return f"The content of the page is: {page_text}"


if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
