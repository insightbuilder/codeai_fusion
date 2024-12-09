# src/code_interpreter_project/crew.py
from crewai import Agent, Task, Crew, Process, LLM
from codeinterpreter_tool import CodeInterpreterTool
import os

llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# Define the agent
code_agent = Agent(
    role="Code Interpreter for a given problem",
    goal="Solve the given problem with python code with given tools and return the results.",
    backstory="A skilled programmer capable of interpreting and running Python scripts.",
    tools=[CodeInterpreterTool()],
    llm=llm,
)


# Define the task
code_execution_task = Task(
    description="""Write the python code for the {problem}, then execute
        the Python code with given tools and return the result.""",
    expected_output="Result of the executed code.",
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
    # inputs = {"problem": "Find the sum of 1, 2, 3, 4"}
    inputs = {"problem": "Find the 10th fibonaccic number"}

    # Run the crew
    result = code_crew.kickoff(inputs=inputs)
    print(result)
