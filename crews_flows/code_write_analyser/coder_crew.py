from crewai import Agent, Crew, Task, LLM
from crewai_tools import FileWriterTool
from pydantic import BaseModel, Field
import os


filewriter_tool = FileWriterTool()
llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

codegen_agent = Agent(
    role="You are a problem solver and code writer",
    goal="Review the {user_query} and write code to solve the problem and return the code",
    backstory="You are a competitive coder, and expert problem solver with a deep understanding of the language",
    llm=llm,
)


class CodeData(BaseModel):
    code: str = Field(default="", description="This is the code for the problem")


codegen_task = Task(
    description="For the {user_query} and write code return it",
    expected_output="Output code",
    agent=codegen_agent,
    output_pydantic=CodeData,
)


data_write_agent = Agent(
    role="You are a data writer",
    goal="Write the code to the given file in the {user_query}",
    backstory="You are very good in formatting and writing the code",
    tools=[filewriter_tool],
    llm=llm,
)

data_write_task = Task(
    description="Write the code to the given file in the {user_query}",
    expected_output="Status of file write completion",
    agent=data_write_agent,
)

codegen_crew = Crew(
    name="codegen_crew",
    agents=[codegen_agent, data_write_agent],
    tasks=[codegen_task, data_write_task],
    verbose=True,
)

code_output = codegen_crew.kickoff(
    {
        "user_query": "Write a python function to find the Greatest Common divisor to ./gcd_function.py"
    }
)

print(code_output.to_dict())
