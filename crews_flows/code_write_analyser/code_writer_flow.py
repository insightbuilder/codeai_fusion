import warnings
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel
from file_analyzer import read_analyse_crew
from coder_crew import codegen_crew
from intent_finder_crew import intent_crew

# ruff: noqa
# from coder_crew import codegen_crew


warnings.filterwarnings("ignore")


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
        if self.state.intent == "write code":
            return "go_code"
        elif self.state.intent == "analyse file":
            return "go_analyse"
        else:
            return "go_other"

    @listen("go_code")
    def make_code(self):
        try:
            codegen_crew_output = codegen_crew.kickoff(
                {"user_query": self.state.user_query}
            )
            print(self.state, "+> writing code to file")
            with open("./codegen_test.py", "w") as f:
                f.write(codegen_crew_output["code"])
            print("check the working directory")
            return {"status": "Code written to file"}
        except Exception as e:
            return {"error": str(e)}

    @listen("go_analyse")
    def make_analysis(self):
        try:
            read_analyse_crew_output = read_analyse_crew.kickoff(
                {"user_query": self.state.user_query}
            )
            print(read_analyse_crew_output["analysis"])  # self.state.analysis
            return {"status": "Analysis done"}
        except Exception as e:
            return {"error": str(e)}

    @listen("go_other")
    def something_else(self):
        # self.state.intent = "other"
        return {"message": "No further action taken for 'other' intent."}
        # return "go_analyse"


if __name__ == "__main__":
    flow = CodeWriterFlow()
    result_of_flow = flow.kickoff(
        {"user_query": "Write a python function to find the Greatest Common divisor"}
        # {"user_query": "Analyse the python file ./analyser_test.py"}
        # {"user_query": "Where is rio located"}
    )

    print("Final result of the flow:", result_of_flow)
