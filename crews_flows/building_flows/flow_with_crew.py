from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from prompt_agents import (
    agent1 as findagent,
    fileagent,
    writertask,
    task1 as findtask,
)
from crewai import Crew

flowcrew = Crew(
    agents=[findagent],
    tasks=[findtask],
    verbose=True,
)


class Input(BaseModel):
    input_data: str = ""
    message: str = ""


class CrewFlow(Flow[Input]):
    @start()
    def first_method(self):
        self.state.input_data = input("Flow assking input: ")
        return self.state.input_data

    @listen(first_method)
    def second_method(self, first_meth_op):
        self.state.message = flowcrew.kickoff({"input": first_meth_op})
        return self.state.message


crewflow = CrewFlow()

crewflow = crewflow.kickoff({"input_data": "Ai Agents"})

print(crewflow)
