from typing import Callable
from composio_openai import ComposioToolSet, action, Action
from openai import OpenAI

openai_client = OpenAI()

toolset = ComposioToolSet()


@action(toolname="github")
def star_repo(
    owner: str,
    repo: str,
    execute_request: Callable,
) -> bool:
    """
    Star a repository for a user.

    :param owner: Name of the owner.
    :param repo: Name of the repository.
    :return success: True if the repository was starred, False otherwise.
    """
    put_res = execute_request(f"/user/starred/{owner}/{repo}", "put", None, None)
    print(type(put_res))  # <class 'dict'>
    print(put_res)  # {'data': '', 'successfull': True}
    return True


tools = toolset.get_tools(actions=[star_repo])

task = "Star the repo kamalabot/cratesploring"

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
