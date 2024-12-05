from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel


class StructState(BaseModel):
    counter: int = 0
    message: str = ""


class RouterFlow(Flow[StructState]):
    @start()
    def first_method(self):
        self.state.counter += 2
        # return self.state.counter

    @router(first_method)
    def move_forward(self):

        if self.state.counter % 2 == 0:
            return "route1"
        else:
            return "route2"

    @listen("route1")
    def move_left(self):
        self.state.message += "moving to left "
        print("Message: ", self.state.message)  # return self.state.message

    @listen("route2")
    def move_right(self):
        self.state.message += "moving to right"
        print("Message: ", self.state.message)  # return self.state.message


justflow = RouterFlow()

justflow.plot("routerflow.png")

rightroute = RouterFlow().kickoff({"counter": 11, "message": ""})
print("Right route: ", rightroute)


leftroute = RouterFlow().kickoff({"counter": 10, "message": ""})
print("Left Route: ", leftroute)
