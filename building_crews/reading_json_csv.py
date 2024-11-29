import os
from crewai import Crew, Agent, Task, Process, LLM
from crewai_tools import JSONSearchTool, CSVSearchTool
from dotenv import load_dotenv

load_dotenv()

groq_llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])

json_tool = JSONSearchTool(json_path="./agent_docs/json_data.json")

csv_tool = CSVSearchTool(csv_path="./agent_docs/csv_data.csv")

json_search_agent = Agent(
    role="You can search json data on when asked by the user",
    goal="Return the json content when asked by the user",
    backstory="You are expert on searching json content",
    tools=[json_tool],
    verbose=True,
    llm=groq_llm,
)

csv_search_agent = Agent(
    role="You can search csv data when asked by the user",
    goal="Return the csv content when asked by the user",
    backstory="You are expert on searching csv content",
    tools=[csv_tool],
    verbose=True,
    llm=groq_llm,
)

search_json = Task(
    description="Search json data of atleast 3 key value pairs",
    expected_output="json data",
    agent=json_search_agent,
)

search_csv = Task(
    description="Search csv data of atleast 3 rows",
    expected_output="csv data",
    agent=csv_search_agent,
)


json_crew = Crew(
    agents=[json_search_agent],
    tasks=[search_json],
    process=Process.sequential,
    verbose=True,
)

csv_crew = Crew(
    agents=[csv_search_agent],
    tasks=[search_csv],
    process=Process.sequential,
    verbose=True,
)
print("Getting json data")
json_crew.kickoff({"topic": "How many purchases jane smith has made?"})

print("Getting csv data")
csv_crew.kickoff({"topic": "How many desk chairs are there?"})
