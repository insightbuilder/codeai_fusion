from composio_crewai import ComposioToolSet, Action
import os
from openai import OpenAI

toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
openai_client = OpenAI()

# connected_account_id = toolset.get_connected_account_id()

tools = toolset.get_tools(actions=["FILETOOL_CREATE_FILE"])

# print(tools[0])
# print(len(tools))


# toolset.execute_action(
#     action=Action.FILETOOL_CREATE_FILE,
#     params={"path": "composio_test.py"},
# )

task = "list the files in the directory with tools"

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task},
    ],
)
print("Response is: {response}")

result = toolset.handle_tool_calls(response)

print(result)
