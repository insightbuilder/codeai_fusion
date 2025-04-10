from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
import httpx

mcp = FastMCP("My App")


@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Dynamic user data"""
    return f"Profile data for user {user_id}"


@mcp.resource("config://app1")
def get_config1() -> str:
    """Static configuration data"""
    return "App configuration here"


@mcp.resource("config://{app}")
def get_config(app: str) -> str:
    """Static configuration data"""
    return f"App configuration here is {app}"


@mcp.resource("local://main")
def get_file() -> str:
    """Static file content"""
    print("Reaching here...")
    with open("./main.py", "r") as f:
        return f.read()


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text


@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]


@mcp.tool()
async def long_task(files: list[str], ctx: Context) -> str:
    """Process multiple files with progress tracking"""
    file_data = ""
    for i, file in enumerate(files):
        await ctx.info(f"Processing {file}")
        await ctx.report_progress(i, len(files))
        data, mime_type = await ctx.read_resource("local://main")
        await ctx.info(f"File type: {mime_type}")
        await ctx.info(f"{data.content}")
        file_data += data.content
    return file_data


if __name__ == "__main__":
    print("Server Starts")
    print(dir(mcp))
    print(mcp.settings)
    mcp.run()
