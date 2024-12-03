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
    file_name: str = ""


class RecipeFlow(Flow[RecipeState]):
    @start()
    def extraction(self):
        extraction_crew_output = Extraction_Crew.kickoff({"input": self.state.input})
        # print("pydantic", extraction_crew_output.pydantic)
        # store the file name
        self.state.file_name = extraction_crew_output.pydantic.file_name
        return extraction_crew_output.pydantic

    @listen(extraction)
    def create_recipe(self, extraction_output):
        # print(f"Extraction in side create {extraction_output}")
        dict_input = extraction_output.dict()
        chef_crew_output = Chef_Crew.kickoff(dict_input)
        return chef_crew_output.pydantic

    @listen(create_recipe)
    def write_recipe(self, create_recipe_out):
        # print(f"Write recipe: {create_recipe_out}")
        to_write = create_recipe_out.dict()
        to_write["file_path"] = self.state.file_name
        print(f"Assembled to_write: {to_write}")
        writer_crew_output = Writer_Crew.kickoff(to_write)
        return writer_crew_output


makerecipe = RecipeFlow()
flow_output = makerecipe.kickoff(
    {
        "input": "Provide the Recipe for rice dumplings to serve 15 people, and write to chef_recipe.md"
    }
)
print(flow_output)
