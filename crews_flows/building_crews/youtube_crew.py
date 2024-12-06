# ruff: noqa F401

from crewai import Agent, Task, Crew, LLM
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
import os

from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

load_dotenv()

groqllm = LLM(
    model="groq/llama3-8b-8192",
    api_key=os.environ["GROQ_API_KEY"],
)

scrape_website_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()

yt_agent = Agent(
    role="You can search youtube videos on when asked by the user on any topic",
    goal="Return a list of 5 youtube video links, and its details on the topic asked by the user",
    backstory="You are expert on searching the internet for youtube videos and organising it in a list",
    tools=[
        search_tool,
        scrape_website_tool,
    ],
    verbose=True,
    # llm=groqllm,
    # the model used is gpt-4
)


class YtVideos(BaseModel):
    links: List[str] = []
    titles: List[str] = []
    # channels: List[str] = []


yt_task = Task(
    description="""Your work is to search youtube videos on the {topic} asked by the user using the tools given,
                Then use the tools to extract the specific details asked about the youtube videos and then return""",
    expected_output="A list of youtube video links, the video title on the {topic} asked by the user",
    agent=yt_agent,
    output_json=YtVideos,
)

ytcrew = Crew(name="youtube_crew", tasks=[yt_task], verbose=True)

yt_data = ytcrew.kickoff({"topic": "How to use AI Agents"})
