from crewai import Crew, Agent, Task, Process
from crewai.memory.enhanced_long_term_memory import EnhancedLongTermMemory
from crewai.memory.enhanced_short_term_memory import EnhancedShortTermMemory
from crewai.memory.enhanced_entity_memory import EnhancedEntityMemory
from crewai.memory.storage import LTMSQLiteStorage, RAGStorage

# Configuration for embeddings
embedder = {
    "model": "text-embedding-ada-002",  # OpenAI's text embedding model
    "dimension": 1536  # Dimension of the embeddings
}

# Define the data directory for memory storage
DATA_DIR = "./memory_storage"

def create_crew_with_memory():
    """
    Creates a CrewAI instance with enhanced memory capabilities:
    1. Long-term Memory: Persistent storage using SQLite
    2. Short-term Memory: RAG-based memory for recent context
    3. Entity Memory: Tracks and maintains information about specific entities
    """
    
    # Initialize memory components
    long_term_memory = EnhancedLongTermMemory(
        storage=LTMSQLiteStorage(
            db_path=f"{DATA_DIR}/long_term_memory.db"
        )
    )

    short_term_memory = EnhancedShortTermMemory(
        storage=RAGStorage(
            crew_name="research_crew",
            storage_type="short_term",
            data_dir=DATA_DIR,
            model=embedder["model"],
            dimension=embedder["dimension"],
        )
    )

    entity_memory = EnhancedEntityMemory(
        storage=RAGStorage(
            crew_name="research_crew",
            storage_type="entities",
            data_dir=DATA_DIR,
            model=embedder["model"],
            dimension=embedder["dimension"],
        )
    )

    # Create example agents
    researcher = Agent(
        name="Researcher",
        role="Research expert",
        goal="Conduct thorough research and analysis",
        backstory="Expert in gathering and analyzing information",
        allow_delegation=True,
        memory=True  # Enable memory for this agent
    )

    writer = Agent(
        name="Writer",
        role="Content writer",
        goal="Create engaging content based on research",
        backstory="Experienced in creating compelling narratives",
        allow_delegation=True,
        memory=True  # Enable memory for this agent
    )

    # Create example tasks
    research_task = Task(
        description="Research the latest developments in AI",
        agent=researcher
    )

    writing_task = Task(
        description="Write a comprehensive report based on the research",
        agent=writer
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
        verbose=True
    )

    return crew

if __name__ == "__main__":
    # Create and run the crew
    crew = create_crew_with_memory()
    result = crew.kickoff()
    print("Crew execution completed:", result)
