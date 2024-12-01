import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileWriterTool
from dotenv import load_dotenv

load_dotenv()

filewrite_tool = FileWriterTool()

# presult = filewrite_tool._run(
#     filename="ytvideo_file.txt",
#     content="This is a youtube video trial",
#     directory="agent_docs",
#     overwrite="False",
# )

# print(presult)
openaillm = LLM(
    model="openai/gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"],
)
just_writer_agent = Agent(
    role="Just a writer",
    goal="write the given data to the file in the given {file_path}",
    backstory="You are a file saving program that stores file on file system",
    tools=[filewrite_tool],
    verbose=True,
    llm=openaillm,
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
        "file_path": "Update the 5 salient features of Youtube  ./agent_docs/update_features.txt"
    }
)
