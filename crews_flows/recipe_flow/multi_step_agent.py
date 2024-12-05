from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import os

llm = LLM(model="groq/gemma2-9b-it", api_key=os.environ["GROQ_API_KEY"])


@tool("translate_to_sql")
def translate_to_sql(nl_query, schema_info):
    """Translate NL query to SQL"""
    return "SELECT email FROM users WHERE name = 'John Doe';"


@tool("execute_sql")
def execute_sql(db_name, query) -> str:
    """Execute SQL query"""
    return "john.doe@example.com"


def step_callback(step_name, result) -> str:
    print(f"Step '{step_name}' result: {result}")
    return result  # Optionally modify


def task_callback(task_name, output):
    print(f"Task '{task_name}' completed with output: {output}")


# Define agent and task
agent = Agent(
    role="SQL Specialist",
    goal="Translate and execute SQL queries",
    tools=[translate_to_sql, execute_sql],
    backstory="You are a SQL Specialist",
    llm=llm,
)
task = Task(
    description="Process NL query and return a conversational result.",
    expected_output="Conversational query result.",
    agent=agent,
    callback=task_callback,
)

# Define crew
crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)

# Execute workflow
inputs = {
    "nl_query": "What is John Doe's email?",
    "schema_info": "Table: users, Columns: id, name, email",
    "db_name": "example.db",
}
result = crew.kickoff(inputs=inputs)
print(result)
