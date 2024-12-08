# pyright: reportMissingImports=false
# pyright: reportCallIssue=false
# pyright: reportAttributeAccessIssue=false

# setting the os.environ.get("CREWAI_STORAGE_DIR")

from crewai import Crew, Agent, Task, Process
from crewai.memory.long_term.long_term_memory import LongTermMemory
from crewai.memory.short_term.short_term_memory import ShortTermMemory
from crewai.memory.entity.entity_memory import EntityMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage
from inspect import getsource

# print(getsource(RAGStorage))
# Configuration for embeddings
embedder = {
    "provider": "openai",
    "model": "text-embedding-ada-002",  # OpenAI's text embedding model
    "dimension": 1536,  # Dimension of the embeddings
}

# Define the data directory for memory storage
DATA_DIR = "./db"


def create_crew_with_memory():
    """
    Creates a CrewAI instance with enhanced memory capabilities:
    1. Long-term Memory: Persistent storage using SQLite
    2. Short-term Memory: RAG-based memory for recent context
    3. Entity Memory: Tracks and maintains information about specific entities
    """

    # Initialize memory components
    long_term_memory = LongTermMemory(
        storage=LTMSQLiteStorage(db_path=f"{DATA_DIR}/long_term_memory.db")
    )

    # Create example agents
    researcher = Agent(
        name="Researcher",
        role="Research expert",
        goal="Conduct thorough research and analysis",
        backstory="Expert in gathering and analyzing information",
        allow_delegation=True,
        memory=True,  # Enable memory for this agent
    )

    writer = Agent(
        name="Writer",
        role="Content writer",
        goal="Create engaging content based on research",
        backstory="Experienced in creating compelling narratives",
        allow_delegation=True,
        memory=True,  # Enable memory for this agent
    )
    short_term_memory = ShortTermMemory(
        storage=RAGStorage(
            type="short_term",
        ),
        embedder_config=embedder,
        # path=f"{DATA_DIR}/short_term_memory.db",
    )

    entity_memory = EntityMemory(
        storage=RAGStorage(
            type="entities",
        ),
        embedder_config=embedder,
        # path=f"{DATA_DIR}/entity_memory.db",
    )

    # Create example tasks
    research_task = Task(
        description="Research the latest developments in AI",
        expected_output="Summary of latest research development",
        agent=researcher,
    )

    writing_task = Task(
        description="Write a comprehensive report based on the research",
        expected_output="Comprehensive report based on the research",
        agent=writer,
    )

    # Assemble the crew with memory capabilities
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        memory=True,  # Enable memory for the crew
        long_term_memory=long_term_memory,
        short_term_memory=short_term_memory,
        entity_memory=entity_memory,
        verbose=True,
    )

    return crew


if __name__ == "__main__":
    # Create and run the crew
    crew = create_crew_with_memory()
    print("Crew execution started...")
    # result = crew.kickoff()
    # print("Crew execution completed:", result)
