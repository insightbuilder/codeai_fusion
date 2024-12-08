# src/code_interpreter_project/crew.py
from crewai import Agent, Task, Crew, Process, LLM

# from codeinterpreter_tool import CodeInterpreterTool
from shell_executor_tool import ShellExecutorTool
from crewai_tools import FileWriterTool
import os

llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])

# Define the agent
code_agent = Agent(
    role="Shell script writer and executor",
    goal="Solve the given problem with shell commands  \
     with given tools and return the results.",
    backstory="A skilled shell script coder capable of \
    automating and using shell commands fluently.",
    tools=[ShellExecutorTool()],
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="File Writer",
    goal="write the code in code fences along with its solution to {output_file} using available tools",
    backstory="You are expert markdown writer, you are excellent in handling tools.",
    tools=[FileWriterTool()],
    verbose=True,
    llm=llm,
)

# Define the task
code_execution_task = Task(
    description="""Write the shell command code for the {problem}, then execute
        the shell code with given tools and return the result.""",
    expected_output="Result of the executed code.",
    agent=code_agent,
)

result_write_task = Task(
    description="""Write the shell command code for the {problem} and its solution to {output_file}.""",
    expected_output="Result of file writing status.",
    agent=writer,
)

# Create the crew
code_crew = Crew(
    agents=[code_agent, writer],
    tasks=[code_execution_task, result_write_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    # Input: Python code to execute
    inputs = {
        "problem": "What are the files in the current directory",
        "output_file": "result/result.md",
    }

    # Run the crew
    result = code_crew.kickoff(inputs=inputs)
    print(result)
