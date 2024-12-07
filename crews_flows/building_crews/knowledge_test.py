from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.base_knowledge_source import BaseKnowledgeSource
from crewai.utilities.converter import re
import requests
from typing import Dict, Any
from pydantic import Field
import os

llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])


class SpaceNewsKnowledgeSource(BaseKnowledgeSource):
    """Knowledge source that fetches data from Space News API."""

    api_endpoint: str = Field(description="API endpoint URL")
    limit: int = Field(default=10, description="Number of articles to fetch")

    def load_content(self) -> Dict[Any, str]:
        """Fetch and format space news articles."""
        print("Loading Content")
        try:
            response = requests.get(f"{self.api_endpoint}?limit={self.limit}")
            response.raise_for_status()

            data = response.json()
            articles = data.get("results", [])

            formatted_data = self._format_articles(articles)
            return {self.api_endpoint: formatted_data}
        except Exception as e:
            raise ValueError(f"Failed to fetch space news: {str(e)}")

    def _format_articles(self, articles: list) -> str:
        """Format articles into readable text."""
        formatted = "Space News Articles:\n\n"
        print(formatted)
        for article in articles:
            formatted += f"""
                Title: {article['title']}
                Published: {article['published_at']}
                Summary: {article['summary']}
                News Site: {article['news_site']}
                URL: {article['url']}
                -------------------"""
        return formatted

    def add(self) -> None:
        """Process and store the articles."""
        content = self.load_content()
        print("Entering Add...")
        for _, text in content.items():
            chunks = self._chunk_text(text)
            self.chunks.extend(chunks)

        # self.save_documents()

    def chunk_num(self):
        return len(self.chunks)

    def chunk_see(self):
        for chunk in self.chunks:
            print(chunk)


# Create knowledge source
recent_news = SpaceNewsKnowledgeSource(
    api_endpoint="https://api.spaceflightnewsapi.net/v4/articles",
    limit=10,
    # embedder={
    #     "provider": "groq",
    #     "config": {"model": "text-embedding-3-small"},
    # },
)

recent_news.add()
print(recent_news.chunk_num())
recent_news.chunk_see()

# Create specialized agent
space_analyst = Agent(
    role="Space News Analyst",
    goal="Answer questions about space news accurately and comprehensively",
    backstory="""You are a space industry analyst with expertise in space exploration, 
    satellite technology, and space industry trends. You excel at answering questions
    about space news and providing detailed, accurate information.""",
    knowledge_sources=[recent_news],
)

# Create task that handles user questions
analysis_task = Task(
    description="Answer this question about space news: {user_question}",
    expected_output="A detailed answer based on the recent space news articles",
    agent=space_analyst,
)

# Create and run the crew
crew = Crew(
    agents=[space_analyst],
    tasks=[analysis_task],
    verbose=True,
    process=Process.sequential,
)

# Example usage
result = crew.kickoff(
    inputs={"user_question": "What is the update on candy toss at jpl as of 2024?"}
)
