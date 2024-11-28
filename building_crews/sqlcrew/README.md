# SQL Crew - Natural Language Database Query System

## Overview
SQL Crew is an AI-powered system built using the CrewAI framework that converts natural language questions into SQL queries. It enables users to interact with SQLite databases using plain English, making database querying accessible to non-technical users.

## Features
- Natural language to SQL conversion
- Intelligent query analysis and optimization
- Schema-aware query generation
- User-friendly result formatting
- Error handling and query validation

## Quick Start

1. **Install Dependencies**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

2. **Configure Environment**
Create `.env` file with:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Run the System**
```bash
python -m src.sqlcrew.main
```

## Documentation
- [Installation Guide](instructions.md#installation)
- [Usage Instructions](instructions.md#usage)
- [Development Guidelines](instructions.md#development-guidelines)
- [Project Overview](project_overview.md)

## Architecture
The system uses a multi-agent approach:
1. Query Analyzer Agent: Understands natural language
2. Schema Expert Agent: Maps to database structure
3. SQL Generator Agent: Creates optimized queries
4. Query Executor Agent: Runs and formats results

## Example Usage
```python
# Sample query
inputs = {
    "nl_query": "How many users are in the database?",
    "schema_info": "Table: users, Columns: id, name, email",
    "db_name": "example.db"
}
```

## Development
See [instructions.md](instructions.md) for detailed development guidelines.

## Requirements
- Python 3.9+
- CrewAI Framework
- SQLite3
- OpenAI API key

## Support
- [CrewAI Documentation](https://docs.crewai.com/)
- [GitHub Issues](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)

## Queries Sent to Cascade

1. Lets build an AI agent based on CrewAI framework. The AI Crew will be tasked with querying a SQLite database. The query will be asked in plain english. The CrewAI Crew will have Agents, Tasks, Tools that will take the plain english question and convert it to structured data, and then query the database. First create project_overview.md and update relevant sections.

2. The crewAI crew has been already created Next we will review the existing folder structure, as the crewAI crew has already been instantiated. In addition refer to @building_crewai_agents.md  and @crewai_tools.md for the development guidelines of agents and tools

3. Review @building_crewai_agents.md development guide and update the instructions.md, Readme.md with correct information regarding the usage, library installation, agent and task files. Include the requirements.txt with the packages to be installed

4. Remove the @instructions.md and update @project_overview.md in its place. Make sure your refer @building_crewai_agents.md development guidelines section for the commands to run the crew. 

5. The @project_overview.md states there are 4 agents, 4 tasks  and 3 tools, which is not correct, Update the file correctly, along with proper description

## License
MIT License