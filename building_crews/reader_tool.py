import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool

readtool = FileReadTool()

# presult = readtool._run(
#     file_path="./agent_docs/makefile.txt",
# )

# print(presult)

# to use the tool, we need a agent rite?

just_reader_agent = Agent(
    role="Just a reader",
    goal="read the file in the given {file_path}",
    backstory="You are expert file reader",
    tools=[readtool],
    verbose=True,
)

print(just_reader_agent.key)

print(just_reader_agent.system_template)

reader_task = Task(
    description="Read the given file and inform what is in",
    expected_output="Add the number of words in the file",
    agent=just_reader_agent,
)

reader_crew = Crew(
    agents=[just_reader_agent],
    tasks=[reader_task],
    process=Process.sequential,
    verbose=True,
)

reader_crew.kickoff({"file_path": "read the file at ./agent_docs/makefile.txt"})
