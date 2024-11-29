import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai_tools import CodeInterpreterTool
from dotenv import load_dotenv

load_dotenv()

groqllm = LLM(
    model="groq/llama3-8b-8192",
    api_key=os.environ["GROQ_API_KEY"],
)

code_interpreter = CodeInterpreterTool(unsafe_mode=True)

coder_agent = Agent(
    role="Coder",
    goal="write the code for the  given {challenge}",
    backstory="You are expert code writer and problem solver",
    verbose=True,
    llm=groqllm,
)

code_executor_agent = Agent(
    role="Versatile code executing agent",
    goal="execute the code given by the coder_agent",
    backstory="You are expert code executor",
    tools=[code_interpreter],
    verbose=True,
    llm=groqllm,
)

write_code = Task(
    description="You have a knack of solving given problems",
    expected_output="code that is written in python that executes",
    agent=coder_agent,
)

execute_task = Task(
    description="Your work is to execute the code",
    expected_output="The result of the executed code",
    agent=code_executor_agent,
)

executor_crew = Crew(
    agents=[coder_agent, code_executor_agent],
    tasks=[write_code, execute_task],
    process=Process.sequential,
    verbose=True,
)

result = executor_crew.kickoff(
    {"challenge": "Provide the 20th fibonacci number by writin the code for it "}
)
