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

code_executor_agent = Agent(
    role="Versatile code executing agent",
    goal="execute the code in the given {code}",
    backstory="You are expert code executor",
    tools=[code_interpreter],
    verbose=True,
    llm=groqllm,
    allow_code_execution=True,
)

execute_task = Task(
    description="Your work is to execute the code",
    expected_output="The result of the executed code",
    agent=code_executor_agent,
)

executor_crew = Crew(
    agents=[code_executor_agent],
    tasks=[execute_task],
    process=Process.sequential,
    verbose=True,
)

result = executor_crew.kickoff({"code": "os.getcwd()\n print('This is executede')"})

print(result)
