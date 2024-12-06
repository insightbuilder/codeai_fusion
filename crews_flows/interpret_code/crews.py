# src/code_interpreter_project/crew.py
from crewai import Agent, Task, Crew, Process
from code_interpreter_tool import code_interpreter

# Define the agent
code_agent = Agent(
    role="Code Interpreter",
    goal="Execute Python code provided by the user and return the results.",
    backstory="A skilled programmer capable of interpreting and running Python scripts.",
    tools=[code_interpreter],
)


# Define the task
code_execution_task = Task(
    description="Execute the given Python code and return the result.",
    expected_output="Result of the executed code.",
    agent=code_agent,
)


# Create the crew
code_crew = Crew(
    agents=[code_agent], tasks=[code_execution_task], process=Process.sequential
)

if __name__ == "__main__":
    # Input: Python code to execute
    inputs = {"code": "result = sum([1, 2, 3, 4])"}

    # Run the crew
    result = code_crew.kickoff(inputs=inputs)
    print(result)
