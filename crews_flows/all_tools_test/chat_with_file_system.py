from pywebio.output import put_text, put_table
from pywebio.input import input
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


# put_text_tools(tools)

put_text("### Lets Get chatting...")

put_table(
    [
        ["Action", "Prompt"],
        ["Change Directory", "Change the directory to /home/uberdev"],
        ["List the files", "List the files in current directory"],
        ["Create a File", "Create a file composio_test.py in current dir"],
        ["List the files", "Check if composio_test.py is there by testing"],
        [
            "Writing content to file",
            "Write the 4 main python frameworks to composio_test.py",
        ],
        [
            "Reading content from file",
            "Read the content of composio_test.py",
        ],
        [
            "Editing the file content",
            "Update the first two lines to transformers and pytorch in composio_test.py",
        ],
    ]
)

while True:
    task = input("User: ")
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        tools=tools,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": task},
        ],
    )
    put_text("Getting response...")
    # put_text(response)

    result = toolset.handle_tool_calls(response)

    put_text("result to change working directory: ", result)
