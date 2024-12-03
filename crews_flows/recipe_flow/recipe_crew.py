# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false

from crewai import Crew, Agent, Task, LLM
from crewai_tools import FileWriterTool
from dotenv import load_dotenv
import os
from pydantic import BaseModel

# flake8: noqa E501

load_dotenv()

llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# declaring the tool instance for file_write_tool

file_write_tool = FileWriterTool(directory=".")

# creating response format


class ExtractFormat(BaseModel):
    dish_name: str = ""
    number_served: int = 5
    file_name: str = ""


# creating extraction agent

extraction_agent = Agent(
    role="You Extract the names of dishes, files, and the quantity or numbers from given input.",
    goal="Extract the details like dish_name, file_name and number of people to be served",
    backstory="You are expert in structuring any prose, and extracting information. You are brief and to the point.",
    llm=llm,
    verbose=True,
)

extraction_task = Task(
    description="Extract the dish_name and number_of_people to be served from {input}",
    expected_output="Json formated dish_name, number_served and file_name",
    agent=extraction_agent,
    output_pydantic=ExtractFormat,
)


def on_extraction_complete(extract):
    print(f"Extraction Output: {extract}")


Extraction_Crew = Crew(
    name="extraction_crew",
    tasks=[extraction_task],
    verbose=True,
    # step_callback=partial(on_extraction_complete, extract="done"),
)


class ChefFormat(BaseModel):
    recipe_data: str


chef_agent = Agent(
    role="Writing recipes for the dishes asked by the users",
    goal="Provide the short to the point recipe for {dish_name} to serve {number_served} with quantity of ingredients to be used",
    backstory="You are michelin star rated Master chef with culinary skills ranging from western to eastern region.You are brief and to the point.",
    llm=llm,
    verbose=True,
)

chef_task = Task(
    description="Write the step by step guide for making {dish_name} to serve {number_served}",
    expected_output="Recipe for the {dish_name} along with quantity of ingredients, in markdown format",
    agent=chef_agent,
    output_pydantic=ChefFormat,
)


def on_recipe_complete(recipe):
    print(f"Chef creating Recipe:{recipe}")


Chef_Crew = Crew(
    name="chef_crew",
    tasks=[chef_task],
    agents=[chef_agent],
    verbose=True,
    # step_callback=partial(on_recipe_complete, recipe="done"),
)

writer_agent = Agent(
    role="""You write the data to the file located at {file_path}
    if file_path is not provided the write to recipe.md file in current directory""",
    goal="Write the text data to the file and update the user on completion",
    backstory="""You are excellent file-system manager, and expert at file writitng.,
    You are brief and to the point.
    You can make the file by using the {file_path} and fill it {recipe_data}""",
    llm=llm,
    tools=[file_write_tool],
    verbose=True,
)

writer_task = Task(
    description="Write the recipe and ingredients to {file_path}",
    expected_output="The status of file writing",
    agent=writer_agent,
)


def on_write_complete():
    print("Writing file: Completed")


Writer_Crew = Crew(
    name="writer_crew", tasks=[writer_task], agents=[writer_agent], verbose=True
)
