from crewai import Agent, Crew, Task, LLM
from pydantic import BaseModel, Field
from crewai_tools import FileReadTool
import os

llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

file_read_tool = FileReadTool()

filepath_agent = Agent(
    role="You are a filepath extracter",
    goal=" Extract the filepath from the {user_query}",
    backstory="You are a file system program very good at extractingg the filepaths",
    llm=llm,
)
