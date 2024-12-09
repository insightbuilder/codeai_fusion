# src/code_interpreter_project/crew.py
from crewai import Agent, Task, Crew, Process, LLM

# from codeinterpreter_tool import CodeInterpreterTool
from shell_executor_tool import ShellExecutorTool
from crewai_tools import FileWriterTool
import os

# llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])
llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# Define the agent
code_agent = Agent(
    role="Shell script writer and executor",
    goal="Solve the {problem} with shell commands  \
     and call the given tools and return the results.",
    backstory="A skilled shell script coder capable of \
    automating and using shell commands fluently.",
    tools=[ShellExecutorTool()],
    llm=llm,
    verbose=True,
)

# Define the task
code_execution_task = Task(
    description="""Write the shell command code for the {problem}, then execute
        the shell code with given tools and return the result.""",
    expected_output="Command for solving the problem and the Result.",
    agent=code_agent,
)


# Create the crew
code_crew = Crew(
    agents=[code_agent],
    tasks=[code_execution_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    # Input: Python code to execute
    inputs = {
        "problem": "Execute the python script basic_exec.py in current directory",
        # "output_file": "result.md",
    }

    # Run the crew
    result = code_crew.kickoff(inputs=inputs)
    print(result)
