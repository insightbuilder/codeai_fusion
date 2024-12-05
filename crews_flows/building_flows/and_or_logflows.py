from crewai.flow.flow import Flow, listen, start, and_, or_


class OrLogFlow(Flow):
    @start()
    def first_method(self):
        self.state["counter"] += 2
        print(f"First method: {self.state['counter']}")

    @listen(first_method)
    def second_method(self, first_meth_op):
        self.state["message"] += f"Result of second_method: {first_meth_op}"
        return self.state["message"]

    @listen(or_(first_method, second_method))
    def logflow(self):
        print("logflow")
        print(self.state)
        return self.state


orflow = OrLogFlow()
orflow = orflow.kickoff({"counter": 5, "message": ""})

print(f"Or Flow output: {orflow}")


class AndLogFlow(Flow):
    @start()
    def first_method(self):
        self.state["counter"] += 2
        return f"First method: {self.state['counter']}"

    @listen(first_method)
    def second_method(self, first_meth_op):
        self.state["message"] += f"Result of second_method: {first_meth_op}"
        return self.state["message"]

    @listen(and_(first_method, second_method))
    def logflow(self):
        print("logflow")
        print(self.state)
        return self.state


andflow = AndLogFlow()
andflow.plot("andflow.png")

andflow = andflow.kickoff({"counter": 5, "message": ""})

print(f"And Flow output: {andflow}")
