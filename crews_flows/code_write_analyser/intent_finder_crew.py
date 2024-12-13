from crewai import Agent, Crew, Task, LLM
import os

# from enum import Enum
from pydantic import BaseModel, Field

# this crew find the intents and places them in a analyser
# code request, and other options.
# llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

llm = LLM(
    model="anthropic/claude-3-haiku-20240307",
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

intent_agent = Agent(
    role="You are a code intent analyser",
    goal="Classify the {user_query} as a Analyse file request, code write request or other request",
    backstory="You are a very good judge of the user intents, and capture their objectives and aims",
    llm=llm,
)


# class IntentEnum(str, Enum):
#     ANALYSE_FILE = "analyse_file"
#     WRITE_CODE = "write_code"
#     OTHER = "other"


class UserIntent(BaseModel):
    intent: str = Field(
        default="other",
        description="The intent of the user query is classified as analyse_file, write_code or other",
    )


intent_task = Task(
    description="Review the {user_query} and classify it into one of the Request types",
    expected_output="Output intent can be analyse file, write code or other intent",
    agent=intent_agent,
    output_pydantic=UserIntent,
)

intent_crew = Crew(
    name="intent_crew",
    tasks=[intent_task],
    verbose=True,
)

if __name__ == "__main__":
    print("Testing intent_crew")
    result = intent_crew.kickoff(
        {"user_query": "Write a python function to find the Greatest Common divisor"}
    )
    print(result.model_dump())
    print(result.to_dict())
    # res1 = intent_crew.kickoff(
    #     {"user_query": "Write a python function to find the Greatest Common divisor"}
    # )

    # assert res1 == {"intent": "write_code"}, print(
    #     "Write code intent did not work", res1
    # )
    # res2 = intent_crew.kickoff(
    #     {"user_query": "Read the ./coder_crew.py and provide a summary"}
    # )
    # assert res2.to_dict() == {"intent": "analyse_file"}, print(
    #     "Analyse file intent did not work", res2
    # )

    # res3 = intent_crew.kickoff({"user_query": "What is the day in the calendar today"})

    # assert res3.to_dict() == {"intent": "other"}, print(
    #     "Other intent did not work", res3
    # )
