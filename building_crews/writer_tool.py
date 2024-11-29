import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileWriterTool
from dotenv import load_dotenv

load_dotenv()

filewrite_tool = FileWriterTool()

presult = filewrite_tool._run(
    filename="makefile.txt",
    content="This is a test",
    directory="agent_docs",
    overwrite="False",
)

print(presult)

just_writer_agent = Agent(
    role="Just a writer",
    goal="write the given data to the file in the given {file_path}",
    backstory="You are a file saving program that stores file on file system",
    tools=[filewrite_tool],
    verbose=True,
)


writer_task = Task(
    description="Write the given data to the file and inform the status",
    expected_output="write status",
    agent=just_writer_agent,
)

writer_crew = Crew(
    agents=[just_writer_agent],
    tasks=[writer_task],
    process=Process.sequential,
    verbose=True,
)

writer_crew.kickoff(
    {
        "file_path": "Update the 5 salient features of R programming to ./agent_docs/rfeatures.txt"
    }
)
