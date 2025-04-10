from composio_openai import ComposioToolSet, Action, action
from openai import OpenAI

openai_client = OpenAI()
toolset = ComposioToolSet()


@action(toolname="cow", requires=["cowsay"])
def my_custom_action(message: str) -> str:
    """
    Cow will say whatever you want it to say.

    :param message: Message to be displayed
    :return greeting: Formatted message.
    """
    import cowsay

    return cowsay.get_output_string("cow", message)


@action(toolname="getmsg_len", requires=[])
def getmsg_len(message: str) -> str:
    """
    Cow will say whatever you want it to say.

    :param message: Message whose length to be returned
    :return msglen: Number of characters in Message.
    """
    return str(len(message))


tools = toolset.get_tools(actions=[getmsg_len])

task = "Say 'AI is the future' using cowsay"

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task},
    ],
)
# print(response.model_dump_json())

result = toolset.handle_tool_calls(response)
print(result[0]["data"]["msglen"])
