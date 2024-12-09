from composio_openai import ComposioToolSet, Action
from openai import OpenAI

from datetime import datetime

openai_client = OpenAI()

composio_toolset = ComposioToolSet(entity_id="testrun")


tools = composio_toolset.get_tools(actions=[Action.GOOGLECALENDAR_CREATE_EVENT])

task = (
    "Create a 1 hour meeting event at 5:30PM IST tomorrow regarding OpenAI Integration"
)

today = datetime.now().strftime("%Y-%m-%d")

response = openai_client.chat.completions.create(
    model="gpt-4-turbo-preview",
    tools=tools,
    messages=[
        {
            "role": "system",
            "content": f"You are a helpful assistant. Today's date is {today}.",
        },
        {"role": "user", "content": task},
    ],
)

result = composio_toolset.handle_tool_calls(response)
print(result)
