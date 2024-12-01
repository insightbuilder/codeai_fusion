from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool

@CrewBase
class DashboardCreationForSlackCasesCrew():
    """DashboardCreationForSlackCases crew"""

    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['data_collector'],
            tools=[ScrapeWebsiteTool()],
        )

    @agent
    def data_visualization_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['data_visualization_expert'],
            tools=[ScrapeWebsiteTool()],
        )


    @task
    def collect_slack_case_data(self) -> Task:
        return Task(
            config=self.tasks_config['collect_slack_case_data'],
            tools=[ScrapeWebsiteTool()],
        )

    @task
    def create_visualizations(self) -> Task:
        return Task(
            config=self.tasks_config['create_visualizations'],
            tools=[ScrapeWebsiteTool()],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the DashboardCreationForSlackCases crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
