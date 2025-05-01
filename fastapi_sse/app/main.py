from fastapi import FastAPI
from app.sse import create_sse_server
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("Echo")

# Mount the Starlette SSE server onto the FastAPI app
app.mount("/", create_sse_server(mcp))
# this mounting allows the sse server to
# handle the reqs to /sse and /message path


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Add MCP functionality with decorators
@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"
