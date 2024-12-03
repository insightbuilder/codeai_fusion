# ruff: noqa
# pyright: reportUnusedVariable=false
# pyright: reportUnusedImport=false
import warnings

warnings.filterwarnings("ignore")
import json
from crewai.flow.flow import Flow, listen, start  # noqa: pyright
from pydantic import BaseModel  # noqa: pyright
from recipe_crew import Chef_Crew, Extraction_Crew, Writer_Crew  # noqa: pyright


class RecipeState(BaseModel):
    input: str = ""
    recipe_data: str = ""


class RecipeFlow(Flow[RecipeState]):
    @start()
    def extraction(self):
        extraction_crew_output = Extraction_Crew.kickoff({"input": self.state.input})
        raw_output = extraction_crew_output.raw
        print("raw_output", raw_output)
        print("pydantic", extraction_crew_output.pydantic)

    @listen(extraction)
    def create_recipe(self, extraction_output):
        print(f"Extraction in side create")
        # chef_crew_output = chef_crew.kickoff(extraction_output)
        # return chef_crew_output

    @listen(create_recipe)
    def write_recipe(self, create_recipe_out):
        print(f"Write recipe:")


makerecipe = RecipeFlow()
flow_output = makerecipe.kickoff(
    {"input": "Recipe for rice dumplings to serve 15 people"}
)
print(flow_output)
