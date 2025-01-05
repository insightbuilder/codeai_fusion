# pyright: reportMissingImports=false

from pydantic_ai import Agent
from pywebio.input import input
from pywebio.output import put_markdown, put_text
import traceback
from rich import print

agent = Agent("openai:gpt-4o-mini", system_prompt="Reply in a single sentence")

put_markdown("## Welcome to basic Pydantic Agent")

while True:
    your_prompt = input("You: ")
    if your_prompt == "" or your_prompt == "bye":
        break
    put_text(f"You: {your_prompt}")
    try:
        result = agent.run_sync(your_prompt)
        put_text(f"Pydantic Agent:  {result.data}")  # print(result.data)

    except Exception as e:
        print(e)
        put_text(traceback.format_exc())
