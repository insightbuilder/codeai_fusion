# pyright: reportMissingImports=false

from pydantic_ai import Agent, RunContext
from pywebio.input import input
from pywebio.output import put_text, put_markdown
import traceback
from typing import Optional


tool_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="Reply in a single sentence, if asked share the tools you have",
)


# Run Context used
@tool_agent.tool
def split_and_count(ctx: RunContext[dict], your_text: Optional[str] = None):
    """Returns the sentence as list of words along with count"""
    cache = ctx.deps
    put_text("Using Tool: split_and_count")
    if not your_text:
        return "Need a sentence to split and count"
    if your_text in cache:
        put_text("Using the Run Context")
        return f"{cache[your_text]['words']} has {cache[your_text]['count']} words"
    split_text = your_text.split(" ")
    count_word = len(split_text)
    put_text("Adding text to Run Context")
    cache[your_text] = {"words": split_text, "count": count_word}
    return f"{split_text} has {count_word} words"


@tool_agent.tool
def word_count(ctx: RunContext[dict], your_text: Optional[str] = None):
    """Returns the just the word count"""
    put_text("Using Tool: word_count")
    if not your_text:
        return "Need a sentence to split and count"
    split_text = your_text.split(" ")
    count_word = len(split_text)
    return f"{your_text} has {count_word} words"


put_markdown("## Welcome to Pydantic Agent with Tool")

# Will be the variable to store the context
cache = {}

while True:
    your_prompt = input("You: ")
    if your_prompt == "" or your_prompt == "bye":
        break
    put_text(f"You: {your_prompt}")
    try:
        result = tool_agent.run_sync(your_prompt, deps=cache)
        put_text(f"Pydantic Agent:  {result.data}")  # print(result.data)

    except Exception as e:
        print(e)
        put_text(traceback.format_exc())
    print("Cache Status: \n")
    print(cache)
