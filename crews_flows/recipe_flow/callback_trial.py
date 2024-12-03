# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false

from crewai import Crew, Agent, Task, LLM, Process
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Any, Dict
from functools import partial

load_dotenv()

llm = LLM(model="groq/gemma2-9b-it", api_key=os.environ["GROQ_API_KEY"])

class ExtractFormat(BaseModel):
    dish_name: str = ""
    number_served: int = 5
    file_name: str = ""

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

def extraction_callback(step_output: Dict[str, Any], **kwargs):
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
    if isinstance(step_output, dict) and 'dish_name' in step_output:
        print(f"Extracted Dish Name: {step_output['dish_name']}")
        print(f"Number to be served: {step_output['number_served']}")
        print(f"File Name: {step_output['file_name']}")

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


def on_recipe_complete(recipe: Dict[str, Any], **kwargs):
    """
    Callback function that will be called after each step in the crew execution
    
    Args:
        step_output: Dictionary containing the output of the current step
        **kwargs: Additional keyword arguments passed to the callback
    """
    print(f"Chef creating Recipe:{recipe}")


Chef_Crew = Crew(
    name="chef_crew",
    tasks=[chef_task],
    verbose=True,
    step_callback=partial(on_recipe_complete, step_chef="done"),
)
Extraction_Crew = Crew(
    name="extraction_crew",
    tasks=[extraction_task, chef_task],
    verbose=True,
    process=Process.sequential,
    step_callback=partial(extraction_callback, step="done"),
)

def test_callback():
    """Test function to demonstrate the callback functionality"""
    test_input = "I want a recipe for Spaghetti Carbonara to serve 4 people"
    
    # Run the crew with the test input
    result = Extraction_Crew.kickoff(inputs={'input': test_input, 'number_served': 4, 'dish_name': 'Spaghetti Carbonara'})
    return result

if __name__ == "__main__":
    result = test_callback()
    print("\nFinal Result:", result)
