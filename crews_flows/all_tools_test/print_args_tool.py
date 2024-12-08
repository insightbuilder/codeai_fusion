from crewai.tools import tool
from crewai_tools import BaseTool
from typing import Any, Type
from crewai import Agent, Task, Crew, LLM
import os

# from pydantic import BaseModel

llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])


@tool("print_args")
def print_args_tool(**kwargs):
    """A tool that prints the arguments passed to it."""
    print(kwargs)
    return kwargs


class PrintArgsTool(BaseTool):
    name: str = "Print Args tools"
    description: str = "A tool that prints the arguments passed to it."

    def _run(self, **kwargs: Any) -> Any:
        print(kwargs)


print_arg_agent = Agent(
    role="You are an expert at printing the python function args in {question}",
    goal="Extract the python function args from the user input",
    backstory="An expert python programmer, and code execution specialist",
    tools=[PrintArgsTool()],
    # tools=[print_args_tool],
    verbose=True,
    llm=llm,
)

print_arg_task = Task(
    description="Extract the python function args from the user input using given tools",
    expected_output="Extracted python function args from the user input",
    agent=print_arg_agent,
)

crew = Crew(
    agents=[print_arg_agent],
    tasks=[print_arg_task],
    verbose=True,
)

result = crew.kickoff(
    {"question": "Argument to be passed to print_args_tool are  a=1, b=2, c=3"}
)
print(result)
