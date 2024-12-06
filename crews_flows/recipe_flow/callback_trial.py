# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false

# ruff: noqa E402

from crewai import Crew, Agent, Task, LLM, Process
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Any, Dict
from crewai_tools import FileWriterTool
from inspect import getsource
from crewai.tasks.task_output import TaskOutput
from crewai.agents.parser import AgentFinish


load_dotenv()

llm = LLM(model="groq/gemma2-9b-it", api_key=os.environ["GROQ_API_KEY"])
write_tool = FileWriterTool()


class ExtractFormat(BaseModel):
    dish_name: str = ""
    number_served: int = 5
    file_name: str = ""


class ChefFormat(BaseModel):
    recipe_data: str


extraction_agent = Agent(
    role="You Extract the names of dishes, files, and the quantity or numbers from given input.",
    goal="Extract the details like dish_name, file_name and number of people to be served",
    backstory="You are expert in structuring any prose, and extracting information. You are brief and to the point.",
    llm=llm,
    # verbose=True,
)

extraction_task = Task(
    description="Extract the dish_name and number_of_people to be served from {input}",
    expected_output="Json formated dish_name, number_served and file_name",
    agent=extraction_agent,
    output_json=ExtractFormat,
)


def extraction_callback(step_output, **kwargs):
    """
    Callback function that will be called after each step in the crew execution

    Args:
        step_output: Dictionary containing the output of the current step
        **kwargs: Additional keyword arguments passed to the callback
    """
    print("\n=== Callback Triggered ===")
    print(f"Step Output: {step_output}")
    print(f"Additional Info: {kwargs}")
    print("========================\n")

    # You can perform any custom processing here
    if isinstance(step_output, dict) and "dish_name" in step_output:
        print(f"Extracted Dish Name: {step_output['dish_name']}")
        print(f"Number to be served: {step_output['number_served']}")
        print(f"File Name: {step_output['file_name']}")


def on_recipe_complete(recipe: Dict[str, Any], **kwargs):
    # recipe is AgentFinish
    """
    Callback function that will be called after each step in the crew execution

    Args:
        step_output: Dictionary containing the output of the current step
        **kwargs: Additional keyword arguments passed to the callback
    """
    print(f"Recipe param type: {type(recipe)}")
    print(f"Chef Agent with {kwargs} creating Recipe:{recipe.output}")


def on_task_complete(task_test: Dict[str, Any], **kwargs):
    """
    Callback function that will be called after task completed

    Args:
        step_output: Dictionary containing the output of the current step
        **kwargs: Additional keyword arguments passed to the callback
    """
    print(f"task_test param type: {type(task_test)}")
    print(f"Chef Task with {kwargs} completed Task:{task_test} ")


chef_agent = Agent(
    role="Writing recipes for the dishes asked by the users",
    goal="Provide the short to the point recipe for {dish_name} to serve {number_served} with quantity of ingredients to be used",
    backstory="You are michelin star rated Master chef with culinary skills ranging from western to eastern region.You are brief and to the point.",
    llm=llm,
    # verbose=True,
    # step_callback=on_recipe_complete,
)


chef_task = Task(
    description="Write the step by step guide for making {dish_name} to serve {number_served}",
    expected_output="Recipe for the {dish_name} along with quantity of ingredients, in markdown format",
    agent=chef_agent,
    output_pydantic=ChefFormat,
    # callback=on_task_complete,
)


Extraction_Crew = Crew(
    name="extraction_crew",
    agents=[extraction_agent, chef_agent],
    tasks=[extraction_task, chef_task],
    # verbose=True,
    process=Process.sequential,
    step_callback=on_recipe_complete,  # should give agent return values, did not get called
    # task_callback=on_task_complete,  # should give task return values, did not get called
)


def test_callback():
    """Test function to demonstrate the callback functionality"""
    test_input = "I want a recipe for Spaghetti Carbonara to serve 4 people save to file ./carbonara.md"

    # Run the crew with the test input
    result = Extraction_Crew.kickoff(
        inputs={
            "input": test_input,
            "number_served": 4,
            "dish_name": "Spaghetti Carbonara",
        }
    )
    return result


if __name__ == "__main__":
    print(getsource(TaskOutput))
    print(getsource(AgentFinish))
    # result = test_callback()
    # print("\nFinal Result:", result)
