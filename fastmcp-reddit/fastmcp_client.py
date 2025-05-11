import asyncio
from typing import Optional

# pyright: reportMissingImports=false
# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false

from fastmcp import Client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

client = Client("http://127.0.0.1:8000/vabired")
anthropic = Anthropic()


async def main():
    async with client:
        ctools = await client.list_tools()
        print(f"Tools are : {[tool.name for tool in ctools]}")
        vabired_system = """You are a profession halreddit, and you know everything about Reddit and its content.
        When you get a query, use the tools provided to you and answer the query. If you are unable to use the 
        tools, then update the user to provide the correct information to use the tools with you. You can also 
        inform the tools you have at your disposal. Use the query provided by the user exactly, don't add your own
        ideas or text to it."""
        while True:
            query = input("Your Query: ")
            if query == "":
                print("Don't give me blank questions: Good Bye.")
                break
            messages = [{"role": "user", "content": query}]
            available_tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema,
                }
                for tool in ctools
            ]

            # Initial Claude API call
            response = anthropic.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1000,
                messages=messages,
                tools=available_tools,
                system=vabired_system,
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
                    result = await client.call_tool(tool_name, tool_args)
                    tool_results.append({"call": tool_name, "result": result})
                    final_text.append(
                        f"[Calling tool {tool_name} with args {tool_args}]"
                    )
                    # print(f"Toolcall Result: {result}")
                    # Continue conversation with tool results
                    if hasattr(content, "text") and content.text:
                        messages.append({"role": "assistant", "content": content.text})
                    messages.append({"role": "user", "content": result})

                    # Get next response from Claude
                    response = anthropic.messages.create(
                        model="claude-3-5-haiku-20241022",
                        max_tokens=1000,
                        messages=messages,
                        system=vabired_system,
                    )

                    final_text.append(response.content[0].text)

            reply = "\n".join(final_text)
            print(f"Your Answer: {reply}")


if __name__ == "__main__":
    asyncio.run(main())
