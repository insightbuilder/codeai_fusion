from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel


class ExampleState(BaseModel):
    counter: int = 0
    message: str = ""


class StructuredFlow(Flow[ExampleState]):
    @start()
    def first_method(self):
        self.state.counter += 2
        return f"First method: {self.state.counter}"

    @listen("first_method")
    def second_method(self, first_meth_op):
        self.state.message += f"Result of second_method: {first_meth_op}"
        self.state.message = "25"
        return self.state.message


struct_flow = StructuredFlow()

struct_flow.plot("structuredflow.png")

flow_out = struct_flow.kickoff()
print(flow_out)
