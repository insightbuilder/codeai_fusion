# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false

from crewai_tools import NL2SQLTool
from crewai import Agent, Crew, LLM, Task
import os

llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# psycopg2 was installed to run this example with PostgreSQL
nl2sql = NL2SQLTool(db_uri="postgresql://postgres:postgres@localhost:5432/testdb")

sqlagent = Agent(
    role="You role is to operate the database to answer {question} with help of the available tools",
    goal="Answer the {question} asked by the user by querying the database",
    backstory="""You are a Database expert with SQL skills. You write 
        and execute SQL queries, based on Natural Language
        requests given to you. You are brief and to the point.""",
    llm=llm,
    verbose=True,
    tools=[nl2sql],
)

sqlcrew = Crew(
    name="sql_crew",
    tasks=[
        Task(
            description="Convert user {question} into SQL queries and get the answer from the database",
            expected_output="SQL query result based on the user question",
            agent=sqlagent,
        )
    ],
    verbose=True,
)

sql_query1 = sqlcrew.kickoff(
    {
        # "question": "Create a table name_register with name, age and email columns and provide status"
        # "question": "Insert bottle, 25 and bottle@table.hall into name_register table and provide status"
        # "question": "Insert name as bottle, age as 25 and email as bottle@table.hall into name_register table and provide status"
        "question": "Provide the data in name_register table"
    }
)

print(sql_query1)
