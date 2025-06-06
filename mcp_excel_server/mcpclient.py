import asyncio
from typing import Optional
from contextlib import AsyncExitStack

# pyright: reportMissingImports=false
# pyright: reportOptionalSubscript=false

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

# uncomment this when running in your local environment
# ensure you have updated the .env file with the Anthropic API Key
# load_dotenv()  # load environment variables from .env


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    # methods will go here
    async def connect_to_server(self, server_script_path: str):
        """Connect to notion MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print(
            "\nConnected to Excel Analysis MCP server with tools:",
            [tool.name for tool in tools],
        )

    async def create_or_connect_db(self):
        import sqlite3

        # Connect to SQLite (creates a file called chatbot.db)
        conn = sqlite3.connect("mcphistory.db")
        cursor = conn.cursor()

        # Create a table to store query-response pairs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            response TEXT NOT NULL
        )
        """)

        conn.commit()
        conn.close()

    async def save_history(self, query: str, response: str):
        import sqlite3

        # Connect to SQLite (creates a file called chatbot.db)
        conn = sqlite3.connect("mcphistory.db")
        cursor = conn.cursor()

        # Insert the query-response pair into the table
        cursor.execute(
            "INSERT INTO conversations (query, response) VALUES (?, ?)",
            (query, response),
        )

        conn.commit()
        conn.close()

    async def read_history(self):
        import sqlite3

        # Connect to SQLite (creates a file called chatbot.db)
        conn = sqlite3.connect("mcphistory.db")
        cursor = conn.cursor()

        # Insert the query-response pair into the table
        cursor.execute("SELECT query, response FROM conversations")

        history = ""

        rows = cursor.fetchall()
        for row in rows:
            history += f"Query: {row[0]}\nResponse: {row[1]}\n{history}\n"

        return history

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""

        hal_system = """You are hal3025, an expert in working on filesystem and excel sheets.
                    You have access to a local filesystem with read and write access.
                    You are very good in analysing xlsx files and you can use the available 
                    tools with you and return the results to the user. 
                    When user asks you to refer to past conversation or history, then refer to 
                    the query and response available with you and respond. Don't say you 
                    do not have access to history.
                    Just use the tools, and provide the updates the tools are giving.
                    Do not use external python packages for the analysis. 
                    Use the tools that are available to you.
                    Do not apologize. Do not provide guidance or examples. Do not share what you cannot do.
                    Please do not provide the python code for the user requests.
                    Do not explain how something can be done."""

        messages = [{"role": "user", "content": query}]

        response = await self.session.list_tools()
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
            system=hal_system,
            messages=messages,
            tools=available_tools,
        )

        # Process response and handle tool calls
        tool_results = []
        final_text = []

        for content in response.content:  # each tool call will handle seperately
            if content.type == "text":
                final_text.append(content.text)
            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # Continue conversation with tool results
                if hasattr(content, "text") and content.text:
                    messages.append({"role": "assistant", "content": content.text})
                messages.append({"role": "user", "content": result.content})

                # Get next response from Claude
                response = self.anthropic.messages.create(
                    model="claude-3-5-haiku-20241022",
                    system=hal_system,
                    max_tokens=1000,
                    messages=messages,
                )

                final_text.append(response.content[0].text)
        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        history = await self.read_history()
        while True:
            try:
                query = input("\nInteract with Excel File here: ").strip()
                # below the history is assembled
                print(history)
                query_with_history = (
                    f"Previous conversation:\n{history}\n Query: {query}"
                )
                if query.lower() == "quit":
                    break

                response = await self.process_query(query_with_history)
                # here is response is apended to history
                await self.save_history(query, response)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        # we use uv package manager so uv run mcpclient.py mcpserver.py
        print("Usage: uv run mcpclient.py server.py")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.create_or_connect_db()
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys

    asyncio.run(main())
