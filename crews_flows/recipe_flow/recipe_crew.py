# Pyright: reportMissingImports=false
# Pyright: reportAttributeAccessIssue=false

from crewai import Crew, Agent, Task, LLM
from crewai_tools import FileWriterTool
from dotenv import load_dotenv
import os
from pydantic import BaseModel

# flake8: noqa E501

load_dotenv()

llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# declaring the tool instance for file_write_tool

file_write_tool = FileWriterTool()

# creating response format


class ExtractFormat(BaseModel):
    dish_name: str
    number_served: int


# creating extraction agent

extraction_agent = Agent(
    role="You Extract the names, quantity from given input.",
    goal="Extract the details like name and number of people to be served",
    backstory="You are expert in structuring any prose, and extracting information. You are brief and to the point.",
    llm=llm,
)

extraction_task = Task(
    description="Extract the dish_name and number_of_people to be served from {input}",
    expected_output="Json formated dish_name and number_served",
    agent=extraction_agent,
    output_pydantic=ExtractFormat,
)

Extraction_Crew = Crew(name="extraction_crew", tasks=[extraction_task], verbose=True)

chef_agent = Agent(
    role="Writing recipes for the dishes asked by the users",
    goal="Provide the detailed recipe for {dish_name} to serve {number_served} with quantity of ingredients to be used",
    backstory="You are michelin star rated Master chef with culinary skills ranging from western to eastern region.You are brief and to the point.",
    llm=llm,
)

chef_task = Task(
    description="Write the step by step guide for making {dish_name} to serve {number_served}",
    expected_output="Recipe for the {dish_name} along with quantity of ingredients, in markdown format",
    agent=chef_agent,
)

Chef_Crew = Crew(
    name="chef_crew",
    tasks=[chef_task],
    agents=[chef_agent],
    verbose=True,
)

writer_agent = Agent(
    role="You write the data to the file located at {file_path}",
    goal="Write the text data to the file and update the user on completion",
    backstory="""You are excellent file-system manager, and expert at file writitng.,
    You are brief and to the point.
    You can make the file by using the {name} and fill it {data}""",
    llm=llm,
    tools=[file_write_tool],
)

writer_task = Task(
    description="Write the recipe and ingredients to {file_path}",
    expected_output="The status of file writing",
    agent=writer_agent,
)

Writer_Crew = Crew(
    name="writer_crew", tasks=[writer_task], agents=[writer_agent], verbose=True
)
