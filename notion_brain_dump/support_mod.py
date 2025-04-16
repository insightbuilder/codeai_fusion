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
