from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from sqlcrew.tools.custom_tool import execute_sql, translate_to_sql


@CrewBase
class Sqlcrew:
    """SQL Crew for natural language database querying"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @before_kickoff
    def validate_inputs(self, inputs):
        """Validate required inputs before starting the crew"""
        required_fields = ['nl_query', 'schema_info', 'db_name']
        missing_fields = [field for field in required_fields if field not in inputs]
        
        if missing_fields:
            raise ValueError(f"Missing required inputs: {', '.join(missing_fields)}")
            
        if not inputs['nl_query'].strip():
            raise ValueError("Natural language query cannot be empty")
            
        if not inputs['schema_info'].strip():
            raise ValueError("Schema information cannot be empty")
            
        if not inputs['db_name'].strip():
            raise ValueError("Database name cannot be empty")

    @agent
    def nl_sql_agent(self) -> Agent:
        """Create the Natural Language SQL Agent"""
        return Agent(
            config=self.agents_config["nl_sql_agent"],
            tools=[translate_to_sql, execute_sql],
            verbose=True,
        )

    @task
    def nl_to_sql_task(self) -> Task:
        """Create the Natural Language to SQL conversion task"""
        return Task(
            config=self.tasks_config["nl_to_sql_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SQL Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    @after_kickoff
    def process_results(self, results):
        """Process and format the crew results"""
        if not results:
            return "No results returned from the crew"
            
        try:
            # Format results for better readability
            if isinstance(results, (list, tuple)):
                return "\n".join(str(result) for result in results)
            return str(results)
        except Exception as e:
            return f"Error processing results: {str(e)}"
