import os
from crewai import LLM, Crew, Agent, Task, Process
from crewai_tools import DirectoryReadTool
from dotenv import load_dotenv

load_dotenv()

groq_llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])
print("Loaded the LLM successfully")

docs_tool = DirectoryReadTool(
    directory="./agent_docs",
)

dir_reader_agent = Agent(
    role="Listing directory",
    goal="read the directory in the given  path and reply to user {question}",
    backstory="You are expert navigating directory trees",
    tools=[docs_tool],
    verbose=True,
    llm=groq_llm,
)

reader_dir = Task(
    description="Read the given directory path and enumerate",
    expected_output="Provide the number of files in the directory",
    agent=dir_reader_agent,
    tools=[docs_tool],
)

crew = Crew(
    agents=[dir_reader_agent],
    tasks=[reader_dir],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(inputs={"question": "How many files are there in the directory"})

print(result)
