from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileWriterTool
from langchain.agents import load_tools
from dotenv import load_dotenv
import os

load_dotenv()

groqllm = LLM(
    model="groq/llama3-8b-8192",
    api_key=os.environ["GROQ_API_KEY"],
)

langchain_tools = load_tools(["google-serper"], llm=groqllm)
# input goes to all the agents
agent1 = Agent(
    role="agent role",
    goal="who is {input}?",
    backstory="agent backstory",
    verbose=True,
)

task1 = Task(
    expected_output="a short biography of {input}",
    description="a short biography of {input}",
    agent=agent1,
)

agent2 = Agent(
    role="agent role",
    goal="summarize the short bio for {input} and if needed do more research",
    backstory="agent backstory",
    verbose=True,
)

task2 = Task(
    description="a tldr summary of the short biography",
    expected_output="5 bullet point summary of the biography",
    agent=agent2,
    context=[task1],
)

filewrite = FileWriterTool()
fileagent = Agent(
    role="File writer agent",
    goal="write the given data to the file in the given {file_path}",
    backstory="You are a file saving program that stores file on file system",
    tools=[filewrite],
    verbose=True,
    llm=groqllm,
)
writertask = Task(
    description="Write the given data to the file and inform the status",
    expected_output="write status",
    agent=fileagent,
)

my_crew = Crew(agents=[agent1, agent2, fileagent], tasks=[task1, task2, writertask])
crew = my_crew.kickoff(
    inputs={"input": "Mark Twain", "file_path": "./agent_docs/mktwain.txt"}
)
