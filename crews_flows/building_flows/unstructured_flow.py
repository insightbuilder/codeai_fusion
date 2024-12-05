from crewai.flow.flow import Flow, listen, start


class UnstructuredFlow(Flow):
    @start()
    def first_method(self):
        # print("Before error", self.state)
        self.state["counter"] += 2
        return f"First method: {self.state['counter']}"

    @listen(first_method)
    def second_method(self, first_meth_op):
        self.state["message"] += f"Result of second_method: {first_meth_op}"
        self.state["newkey"] = "new value"
        return self.state


unstruc_flow = UnstructuredFlow()
flow_out = unstruc_flow.kickoff(
    {
        "counter": 10,
        "message": "Hello, ",
    }
)

print(flow_out)
