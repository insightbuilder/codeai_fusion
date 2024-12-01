from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SeleniumScrapingTool

@CrewBase
class WhatsappChatScrapingCrew():
    """WhatsappChatScraping crew"""

    @agent
    def WhatsAppScraper(self) -> Agent:
        return Agent(
            config=self.agents_config['WhatsAppScraper'],
            tools=[SeleniumScrapingTool()],
        )


    @task
    def navigate_to_whatsapp_task(self) -> Task:
        return Task(
            config=self.tasks_config['navigate_to_whatsapp_task'],
            tools=[SeleniumScrapingTool()],
        )

    @task
    def scrape_messages_task(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_messages_task'],
            tools=[SeleniumScrapingTool()],
        )

    @task
    def save_json_file_task(self) -> Task:
        return Task(
            config=self.tasks_config['save_json_file_task'],
            tools=[SeleniumScrapingTool()],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the WhatsappChatScraping crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
