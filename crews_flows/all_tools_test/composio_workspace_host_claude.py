from pywebio.output import put_text
from composio_openai import ComposioToolSet, WorkspaceType, App, Action
import os

import anthropic

client = anthropic.Anthropic()


toolset = ComposioToolSet(
    workspace_config=WorkspaceType.Host(),
    api_key=os.getenv("COMPOSIO_API_KEY"),
)

tools = toolset.get_tools(apps=[App.FILETOOL])

put_text("### Anthropic Human Prompt")
put_text(anthropic.HUMAN_PROMPT)
put_text("### Anthropic AI Prompt")
put_text(anthropic.AI_PROMPT)

response = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=500,
    tools=tools,
    messages=[
        {"role": "user", "content": "List the files in current directory"},
    ],
)

put_text(response)

result = toolset.handle_tool_calls(response)

# put_text("result for listing dir: ", result)
put_text("Listing files in current directory: ", os.getcwd())
