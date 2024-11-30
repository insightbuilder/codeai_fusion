from crewai.flow.flow import Flow, listen, start


class UnstructuredFlow(Flow):
    @start()
    def first_method(self):
        self.state["counter"] += 2
        return f"First method: {self.state['counter']}"

    @listen(first_method)
    def second_method(self, first_meth_op):
        self.state["message"] += f"Result of second_method: {first_meth_op}"
        return self.state["message"]


unstruc_flow = UnstructuredFlow()
flow_out = unstruc_flow.kickoff({"counter": 10, "message": "Kick Start. \n"})

print(flow_out)
