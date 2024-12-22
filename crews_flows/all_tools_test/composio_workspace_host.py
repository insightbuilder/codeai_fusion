# from composio_crewai import ComposioToolSet, WorkspaceType, Action, App
# the LLM has to be used for operating on the workspace

from composio_openai import ComposioToolSet, WorkspaceType, App, Action
import os
from openai import OpenAI
from rich import print

openai_client = OpenAI()
toolset = ComposioToolSet(
    workspace_config=WorkspaceType.Host(),
    api_key=os.getenv("COMPOSIO_API_KEY"),
)

tools = toolset.get_tools(apps=[App.FILETOOL])


def print_tools(tools):
    for tool in tools:
        # print(type(tool))
        print(tool["function"]["name"])
        # print(tool["function"]["parameters"].keys())
        if "required" in tool["function"]["parameters"]:
            print("required: ", tool["function"]["parameters"]["required"])
            print("title: ", tool["function"]["parameters"]["title"])
            print("properties: ", tool["function"]["parameters"]["properties"])
        else:
            print("No required fields")


# response = openai_client.chat.completions.create(
#     model="gpt-4o-mini",
#     tools=tools,
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Change directory to /home/uberdev"},
#     ],
# )

# # print(response)

# result = toolset.handle_tool_calls(response)

# print("result to change working directory: ", result)

# response = openai_client.chat.completions.create(
#     model="gpt-4o-mini",
#     tools=tools,
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "list the files in the directory"},
#     ],
# )

# # print(response)

# result = toolset.handle_tool_calls(response)

# print("result for listing dir: ", result)


toolset.execute_action(
    action=Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
    params={"path": "/home/uberdev"},
    # Natural language prompt
    # text="change directory to /home/uberdev",
)
toolset.execute_action(
    action=Action.FILETOOL_LIST_FILES,
    params={},
    # Natural language prompt
    text="list the files in the directory",
)
