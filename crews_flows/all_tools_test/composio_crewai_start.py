from composio import App
from crewai_tools import ComposioTool
from crewai import Agent, Task, LLM
import os

# from composio import Action
# from inspect import getsource

llm = LLM(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
# print(getsource(Action))
# tools = [ComposioTool.from_action()]
# tools = ComposioTool.from_app(App.GITHUB, tags=["important"])
tools = ComposioTool.from_app(App.GITHUB, use_case="Star a github repository ")

# print(tools[0])
crewai_agent = Agent(
    role="Github Agent",
    goal="You take action on Github using Github APIs",
    backstory=(
        "You are AI agent that is responsible for taking actions on Github "
        "on users behalf. You need to take action on Github using Github APIs"
    ),
    verbose=True,
    tools=tools,
    llm=llm,
)

task = Task(
    description="Star a repo crewAIInc/crewAI on GitHub",
    agent=crewai_agent,
    expected_output="if the star happened",
)

result = task.execute()
print(result)
