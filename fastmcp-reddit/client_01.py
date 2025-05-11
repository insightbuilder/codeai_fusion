import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from inspect import getsource

# pyright: reportMissingImports=false
# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    # methods will go here
    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        print("Starting Server from within client")
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
        )
        print("This is where the server is running")
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        # print("got the transport...", stdio_transport)
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()
        print("session initialized")

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        # Need to get tools output if the server is up
        print("\nConnected to server with tools:", [tool.name for tool in tools])

        # below code is used initially for testing the read_resource method
        resource_test = await self.session.read_resource("subreddit://info")
        print("Testing Resource in Client side:", resource_test)

        # listing available prompts
        response = await self.session.list_prompts()
        prompts = response.prompts
        print("\nAvailable prompts:", [prompt.name for prompt in prompts])

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        # get the tools
        response = await self.session.list_tools()

        messages = [{"role": "user", "content": query}]
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

        # Initial Claude API call
        response = self.anthropic.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
        )

        # Process response and handle tool calls
        tool_results = []
        final_text = []

        for content in response.content:
            if content.type == "text":
                final_text.append(content.text)
            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                print(f"Tool result call: {result.content}")
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # Continue conversation with tool results
                if hasattr(content, "text") and content.text:
                    messages.append({"role": "assistant", "content": content.text})
                messages.append({"role": "user", "content": result.content})

                # Get next response from Claude
                response = self.anthropic.messages.create(
                    model="claude-3-5-haiku-20241022",
                    max_tokens=1000,
                    messages=messages,
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("Type your market research queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: uv run client.py server.py")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


# Server code that fails, kept here for reference
# @mcp.tool()
# async def get_subreddit_info(query: str) -> Iterable[ReadResourceContents]:
# async def get_subreddit_info(query: str) -> str:
# """Answer the user query by accessing the subreddit_info from
# get_subreddit resource. Use the reply_with_context prompt"""

# data = await mcp.read_resource("subreddit://info")
# # making the prompt
# prompt = mcp.get_prompt(
#     "reply_with_context",
#     arguments={"context": data.contents[0].text, "query": query},
# )
# returning the reply.
# return prompt.messages[0].content.text
# return data
# return data[0].content

# @mcp.tool()
# async def get_resources() -> str:
#     """Returns the list of resources available with you"""
#     resource_list = await mcp.list_resources()
#     res_list_str = ",".join([res.name for res in resource_list])
#     return f"Available resources with you are: {res_list_str}"

if __name__ == "__main__":
    import sys

    asyncio.run(main())
