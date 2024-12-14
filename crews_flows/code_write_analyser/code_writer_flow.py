import warnings
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

warnings.filterwarnings("ignore")
# ruff: noqa
# from coder_crew import codegen_crew

from file_analyzer import read_analyse_crew
from coder_crew_composio_write import codegen_crew
from intent_finder_crew import intent_crew


class CodeWriterState(BaseModel):
    user_query: str = ""
    intent: str = ""
    code: str = ""
    analysis: str = ""


class CodeWriterFlow(Flow[CodeWriterState]):
    @start()
    def intent_extractor(self):
        intent_crew_output = intent_crew.kickoff({"user_query": self.state.user_query})
        self.state.intent = intent_crew_output["intent"]
        print(self.state, "+> Inside intent_extractor")
        return intent_crew_output["intent"]

    @router(intent_extractor)
    def analyze_code_router(
        self,
    ):
        print(self.state, "+> Inside Router")
        if self.state.intent == "write code":
            return "go_code"
        elif self.state.intent == "analyse file":
            return "go_analyse"
        else:
            return "go_other"

    @listen("go_code")
    def go_code(self):
        codegen_crew_output = codegen_crew.kickoff(
            {"user_query": self.state.user_query}
        )
        self.state.code = codegen_crew_output["code"]
        print(self.state, "+> Inside go_code")
        return codegen_crew_output

    @listen("go_analyse")
    def go_analyse(self):
        read_analyse_crew_output = read_analyse_crew.kickoff(
            {"user_query": self.state.user_query}
        )
        self.state.analysis = read_analyse_crew_output.analysis
        print(self.state, "+> Inside go_analyse")
        return read_analyse_crew_output.analysis

    @listen("go_other")
    def go_other(self):
        self.state.intent = "other"
        print(self.state, "+> Inside go_other")
        return "other"


if __name__ == "__main__":
    flow = CodeWriterFlow()
    result_of_flow = flow.kickoff(
        {"user_query": "Write a python function to find the Greatest Common divisor"}
    )

    print(result_of_flow)
