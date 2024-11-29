import os
from crewai import Agent, Task, Crew
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool,
)
from dotenv import load_dotenv
from crewai import Process

load_dotenv()

docs_tool = DirectoryReadTool(
    directory="./agent_docs",
)

files_tool = FileReadTool()

search_tool = SerperDevTool()

web_req_tool = WebsiteSearchTool()

ai_agent_researcher = Agent(
    role="AI Agent Researcher",
    goal="Provider up-to-date market analysis of the AI industry",
    backstory="An expert market researcher",
    tools=[search_tool, web_req_tool],
    verbose=True,
)

writer = Agent(
    role="Writer",
    goal="Create a blog post based on market analysis",
    backstory="An expert writer",
    tools=[files_tool, docs_tool],
    verbose=True,
)

research = Task(
    description="Research the latest trends in the AI Industry and provided a summary",
    expected_output="A summary of the top 3 trending development in the AI industry with a unique perspective on their significance",
    agent=ai_agent_researcher,
)

write = Task(
    description="Write an engaging blog post based on market analysis",
    expected_output="A 4-paragraph blog post formatted in markdown with  markdown with engaging, informative, and accessible content, avoiding complex jargon.",
    agent=writer,
    output_file="blog.md",
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    process=Process.sequential,
    verbose=True,
    planning=True,
)

crew.kickoff()
