from pydantic_ai import Agent
from rich import print
from pywebio.input import input
from pywebio.output import put_text, put_markdown
import traceback

# pyright: reportMissingImports=false
# pyright: reportOptionalMemberAccess=false

memory_agent = Agent("openai:gpt-4o-mini", system_prompt="Reply in a single sentence")

put_markdown("## Welcome to Pydantic Agent with Memory")

result = None
while True:
    your_prompt = input("You: ")
    if your_prompt == "" or your_prompt == "bye":
        break
    put_text(f"You: {your_prompt}")

    if (your_prompt == "show_memory") and result:
        put_text("All Memory:")
        put_text(result.all_messages_json())
    elif (your_prompt == "current_memory") and result:
        put_text("Current Memory:")
        put_text(result.new_messages_json())
    else:
        try:
            if result:
                # First run the result is none, so checking before proceeding
                result = memory_agent.run_sync(
                    your_prompt, message_history=result.all_messages()
                )
            else:
                result = memory_agent.run_sync(your_prompt)

            put_text(f"Pydantic Agent:  {result.data}")  # print(result.data)

        except Exception as e:
            print(e)
            put_text(traceback.format_exc())
