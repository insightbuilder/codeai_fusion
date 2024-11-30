from crewai import Agent, Crew, Task, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import os

content = "Users name is John. He is 30 yearls old and lives in San Francisco"

...
string_source = StringKnowledgeSource(
    content="Users name is John. He is 30 years old and lives in San Francisco.",
    metadata={"preference": "personal"},
)
crew = Crew(...)


llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])

string_source = StringKnowledgeSource(
    content=content,
    metadata={
        "preference": "personal",
    },
)

agent = Agent(
    role="About User",
    goal="You know everything about the user",
    backstory="You are master at understanding people and their data",
    verbose=True,
    llm=llm,
)

task = Task(
    description="Answer the following question about the user: {question}",
    expected_output="An answer to the question",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge={
        "sources": [string_source],
        "metadata": {"preference": "personal"},
        "embedder_config": {
            "provider": "openai",
            "config": {"model": "text-embedding-3-small"},
        },
    },
)

result = crew.kickoff(inputs={"question": "Which is the city John lives?"})
