from composio_crewai import App, ComposioToolSet
from crewai import Agent, Task, LLM, Crew
import os

# pip install composio_crewai composio_core composio_openai
# from inspect import getsource
toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
llm = LLM(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
tools = toolset.get_tools(apps=[App.GITHUB])

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

crew = Crew(
    agents=[crewai_agent],
    tasks=[task],
    verbose=True,
)

result = crew.kickoff()
print(result)
