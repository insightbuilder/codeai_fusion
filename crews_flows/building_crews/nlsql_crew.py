# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false

from crewai_tools import NL2SQLTool
from crewai import Agent, Crew, LLM, Task
from dotenv import load_dotenv
import os   

llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# psycopg2 was installed to run this example with PostgreSQL
nl2sql = NL2SQLTool(db_uri="sqlite:///./sales_database.db")

sqlagent= Agent(
        role="You role is to convert {query} given in natural language queries into native SQL queries",
        goal="Convert natural language query into SQL and query the database",
        backstory="You are a Database expert with SQL skills. You are brief and to the point.",
        llm=llm,
        verbose=True, 
        allow_delegation=False,
        tools=[nl2sql]
    )

sqlcrew = Crew(
    name="sql_crew",
    tasks=[Task(
        description="Convert user {query} into SQL queries and query database", 
        expected_output="Query Results for the database", 
        agent=sqlagent
        )],
    verbose=True,
    process=Process.sequential,
)

sql_query1 = sql_crew.kickoff({"query": "Create a table name_register with name, age and email columns"})

print(sql_query1)