from crewai_tools import SpiderTool
from crewai import Agent, Task, Crew, LLM
import os


def main():
    spider_tool = SpiderTool()

    llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])
    searcher = Agent(
        role="Web Research Expert",
        goal="Find related information from specific URL's",
        backstory="An expert web researcher that uses the web extremely well",
        tools=[spider_tool],
        verbose=True,
        llm=llm,
    )

    return_metadata = Task(
        description="Scrape https://spider.cloud with a limit of 1 and enable metadata",
        expected_output="Metadata and 10 word summary of spider.cloud",
        agent=searcher,
    )

    crew = Crew(
        agents=[searcher],
        tasks=[
            return_metadata,
        ],
        verbose=True,
    )

    crew.kickoff()


if __name__ == "__main__":
    main()
