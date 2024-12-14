from crewai import Agent, Crew, Process, Task, LLM
from pydantic import BaseModel, Field
from crewai_tools import FileReadTool
import os

llm = LLM(
    model="anthropic/claude-3-haiku-20240307", api_key=os.environ["ANTHROPIC_API_KEY"]
)

# llm = LLM(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

file_read_tool = FileReadTool()

filepath_agent = Agent(
    role="You are a filepath extracter",
    goal=" Extract the filepath from the {user_query}",
    backstory="You are a file system program very good at extractingg the filepaths",
    llm=llm,
)


class FilePath(BaseModel):
    file_path: str = Field(default="", description="This is the filepath to the file")


filepath_task = Task(
    description="Extract the filepath from the {user_query}",
    expected_output="Output filepath",
    agent=filepath_agent,
    output_pydantic=FilePath,
)

# filepath_crew = Crew(
#     name="file_path crew",
#     tasks=[filepath_task],
#     verbose=True,
# )

analyser_agent = Agent(
    role="You are a file data analyser",
    goal="Open the file with tools given to you and the Analyse the content",
    backstory="You are having decades of reading files and explaining its content plainly",
    tools=[FileReadTool()],
    llm=llm,
)


class ContentAnalysis(BaseModel):
    analysis: str = Field(
        default="Content is empty",
        description="This is the analysis of the file content",
    )


analyser_task = Task(
    description="Analyse the file and explain the content from the file",
    expected_output="Explanation of the content",
    agent=analyser_agent,
    output_pydantic=ContentAnalysis,
)

# analyser_crew = Crew(
#     name="analyser_crew",
#     tasks=[analyser_task],
#     verbose=True,
# )

read_analyse_crew = Crew(
    name="read_analyse_crew",
    agents=[filepath_agent, analyser_agent],
    tasks=[filepath_task, analyser_task],
    verbose=True,
    process=Process.sequential,
)

if __name__ == "__main__":
    output = read_analyse_crew.kickoff(
        {"user_query": "Analyse the content of ./analyser_test.py"}
    )

    print(output.to_dict())
