from crewai import Crew, Agent, Task
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Any, Dict
from functools import partial

load_dotenv()

llm = None
# llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

nollm_agent = Agent(
    role="Writing recipes for the dishes asked by the users",
    goal="Provide the short to the point recipe for {dish_name} to serve {number_served} with quantity of ingredients to be used",
    backstory="You are michelin star rated Master chef with culinary skills ranging from western to eastern region.",
    llm=None,
    verbose=True,
)

nollm_task = Task(
    description="Write the step by step guide for making ",
    expected_output="Just a task",
    agent=nollm_agent,
)

nollm_crew = Crew(
    name="nollm_crew",
    tasks=[nollm_task],
    verbose=True,
)

nollm = nollm_crew.kickoff()
print(f"No LLM in Loop: {nollm}")
