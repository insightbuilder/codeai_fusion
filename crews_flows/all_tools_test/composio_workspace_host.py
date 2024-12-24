# from composio_crewai import ComposioToolSet, WorkspaceType, Action, App
# the LLM has to be used for operating on the workspace
from pywebio.output import put_text
from composio_openai import ComposioToolSet, WorkspaceType, App, Action
import os
from openai import OpenAI

# from rich import put_text

openai_client = OpenAI()
toolset = ComposioToolSet(
    workspace_config=WorkspaceType.Host(),
    api_key=os.getenv("COMPOSIO_API_KEY"),
)

tools = toolset.get_tools(apps=[App.FILETOOL])


def put_text_tools(tools):
    for tool in tools:
        # put_text(type(tool))
        put_text(tool["function"]["name"])
        # put_text(tool["function"]["parameters"].keys())
        if "required" in tool["function"]["parameters"]:
            put_text("required: ", tool["function"]["parameters"]["required"])
            put_text("title: ", tool["function"]["parameters"]["title"])
            put_text("properties: ", tool["function"]["parameters"]["properties"])
        else:
            put_text("No required fields")


# response = openai_client.chat.completions.create(
#     model="gpt-4o-mini",
#     tools=tools,
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Change directory to /home/uberdev"},
#     ],
# )

# # put_text(response)

# result = toolset.handle_tool_calls(response)

# put_text("result to change working directory: ", result)

# response = openai_client.chat.completions.create(
#     model="gpt-4o-mini",
#     tools=tools,
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "list the files in the directory"},
#     ],
# )

# # put_text(response)

# result = toolset.handle_tool_calls(response)

# put_text("result for listing dir: ", result)
put_text("Listing files in current directory: ", os.getcwd())

toolset.execute_action(
    action=Action.FILETOOL_LIST_FILES,
    params={},
    # Natural language prompt
    # text="list the files in the directory",
)

put_text("Changing directory to /home/uberdev")

toolset.execute_action(
    action=Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
    params={"path": "/home/uberdev"},
    # Natural language prompt
    # text="change directory to /home/uberdev",
)

put_text("Now the current directory: ", os.getcwd())

put_text("Listing files in current directory: ")

toolset.execute_action(
    action=Action.FILETOOL_LIST_FILES,
    params={},
    # Natural language prompt
    # text="list the files in the directory",
)

put_text("Creating the file")

toolset.execute_action(
    action=Action.FILETOOL_CREATE_FILE,
    params={"path": "composio_test.py"},
)

put_text("Adding content to file")

toolset.execute_action(
    action=Action.FILETOOL_WRITE,
    params={
        "file_path": "composio_test.py",
        "text": "put_text('hello world')\nprint('super nova')\nprint('make give')",
    },
)

put_text("Opening the file")

toolset.execute_action(
    action=Action.FILETOOL_OPEN_FILE,
    params={"file_path": "composio_test.py"},
)

put_text("Editing the file")

toolset.execute_action(
    action=Action.FILETOOL_EDIT_FILE,
    params={
        "file_path": "composio_test.py",
        "start_line": 0,
        "end_line": 2,
        "text": "#This is a comment",
    },
)
