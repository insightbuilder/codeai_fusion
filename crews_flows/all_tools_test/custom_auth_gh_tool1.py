from typing import Callable
from composio_openai import ComposioToolSet, action, Action
from openai import OpenAI

openai_client = OpenAI()
toolset = ComposioToolSet()


@action(toolname="github")
def list_repositories(
    owner: str,
    execute_request: Callable,
) -> list[str]:
    """
    List repositories for a user.

    :param owner: Name of the owner.
    :return repositories: List of repositories for given user.
    """
    return [
        repo["name"]
        for repo in execute_request(f"/users/{owner}/repos", "get", None, None).get(
            "data", []
        )
    ]


tools = toolset.get_tools(actions=[list_repositories])

task = "List all the repositories for the organization kamalabot"

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task},
    ],
)

result = toolset.handle_tool_calls(response)

print(result)
