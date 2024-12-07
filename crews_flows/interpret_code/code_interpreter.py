import os
from crewai import LLM, Agent, Task, Crew
from crewai_tools import CodeInterpreterTool
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

groqllm = LLM(
    model="groq/llama3-8b-8192",
    api_key=os.environ["GROQ_API_KEY"],
)

code_interpreter = CodeInterpreterTool()

code_executor_agent = Agent(
    role="Versatile code writing, interpreting and executing agent",
    goal="execute the code in the given {problem}",
    backstory="You are expert code executor",
    tools=[code_interpreter],
    verbose=True,
    llm=groqllm,
    allow_code_execution=True,
    code_execution_mode="safe",
)


class CodeResult(BaseModel):
    result: str


execute_task = Task(
    description="Your work is to write code on given {problem} and then execute the code with tools available",
    expected_output="The result of the executed code",
    agent=code_executor_agent,
)

executor_crew = Crew(
    agents=[code_executor_agent],
    tasks=[execute_task],
    # process=Process.sequential,
    verbose=True,
)

result = executor_crew.kickoff(
    {"problem": "Get the current working directory of this program"}
)

print(result)
