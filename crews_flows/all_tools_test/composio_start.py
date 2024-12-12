from composio_openai import ComposioToolSet, App
from openai import OpenAI
from inspect import getsource

print(getsource(ComposioToolSet))

# from crewai_tools import ComposioTool

openai_client = OpenAI()
composio_toolset = ComposioToolSet()

git_tools = composio_toolset.get_tools(apps=[App.GITHUB])

# print(git_tools[0])
# print(git_tools[0]["function"]["name"])
# print(len(git_tools))

task = "Star the repo crewAIInc/crewAI-tools on github"

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    tools=git_tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": task},
    ],
)

print("recieved response...", response)

# result = composio_toolset.handle_tool_calls(response)
# print(result)
