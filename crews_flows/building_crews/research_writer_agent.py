from crewai import Crew, Process, Agent, Task, LLM
from crewai_tools import SerperDevTool, FileWriterTool

import os

llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])

# Define your agents
researcher = Agent(
    role="Your work is to be the best in class Researcher",
    goal="Conduct foundational research with the available tools on given {topic}",
    tools=[SerperDevTool()],
    backstory="An experienced researcher with a passion for uncovering insights",
    verbose=True,
)

writer = Agent(
    role="Your role is to Write the data to the file system to {file_name} using the tools",
    goal="Write the final report to the file",
    backstory="A skilled writer with a talent for crafting compelling narratives",
    tools=[FileWriterTool()],
    verbose=True,
)

# Define your tasks
research_task = Task(
    description="Gather relevant data on the {topic}",
    agent=researcher,
    expected_output="A report of 2 paragraphs, detailing the current advancements in {topic}",
)

writing_task = Task(
    description="Write the data from the researcher to the {file_name}",
    agent=writer,
    expected_output="Status on file written to system",
)

# Form the crew with a sequential process
report_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True,
)

# Execute the crew
inputs = {"topic": "Advances in Agentic IDE", "file_name": "report/Agentic_ide.md"}
result = report_crew.kickoff(inputs=inputs)
