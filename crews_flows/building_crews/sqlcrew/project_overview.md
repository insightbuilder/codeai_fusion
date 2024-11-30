# SQL Crew - Natural Language to SQL Query System

## Project Overview
SQL Crew is an AI-powered system built using the CrewAI framework that converts natural language questions into SQL queries and executes them against a SQLite database. The system employs an intelligent agent working together with specialized tools to understand, process, and execute database queries.

## Installation and Setup

1. Create and activate a virtual environment:
```bash
python -m venv crewenv
source crewenv/bin/activate  # On Windows: crewenv\Scripts\activate
```

2. Install required packages:
```bash
pip install crewai crewai-tools
```

3. Set up environment variables:
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## System Architecture

### Agent
**Natural Language SQL Agent**
- **Role**: Expert in converting natural language questions into precise SQL queries
- **Goal**: Convert user questions into correct SQL queries and provide user-friendly results
- **Capabilities**:
  - Natural language understanding
  - SQL query generation
  - Schema analysis
  - Query optimization
  - Result formatting
- **Behaviors**:
  - Input validation and edge case handling
  - Clarification requests for ambiguous queries
  - Helpful error messaging
  - Result formatting for readability
  - SQL injection prevention
  - Query optimization

### Task
**Natural Language to SQL Task**
- **Description**: Process natural language queries through:
  1. Schema analysis
  2. Query conversion
  3. Query execution
  4. Result formatting
- **Expected Output**:
  1. Interpreted SQL query
  2. Query results in human-readable format
  3. Explanations and context
  4. Error messages or clarification requests if needed

### Tools
1. **translate_to_sql**
   - Converts natural language queries to SQL statements
   - Uses schema information for accurate translation
   - Handles various query types (SELECT, COUNT, etc.)
   - Returns well-formed SQL or error message

2. **execute_sql**
   - Executes SQL queries against SQLite database
   - Formats results with column names
   - Handles errors gracefully
   - Returns formatted results or error messages

## Project Structure
```
sqlcrew/
├── src/
│   └── sqlcrew/
│       ├── config/
│       │   ├── agents.yaml    # Agent definition
│       │   └── tasks.yaml     # Task definition
│       ├── tools/
│       │   └── custom_tool.py # Tool implementations
│       ├── crew.py           # Main crew implementation
│       └── main.py           # Entry point
├── tests/
├── .env                      # Environment variables
└── requirements.txt          # Package dependencies
```

## Running the Crew

1. Create your crew:
```bash
crewai create crew sqlcrew
```

2. Update configuration files:
- Modify `src/sqlcrew/config/agents.yaml` for agent definition
- Modify `src/sqlcrew/config/tasks.yaml` for task definition
- Update `src/sqlcrew/crew.py` for crew logic and tools

3. Run the crew:
```bash
crew run
```

## Usage Example
```python
inputs = {
    "nl_query": "How many users are in the database?",
    "schema_info": """
        Table: users
        Columns:
        - id (INTEGER PRIMARY KEY)
        - name (TEXT NOT NULL)
        - email (TEXT UNIQUE NOT NULL)
    """,
    "db_name": "example.db"
}
```

## Technology Stack
- Python 3.9+
- CrewAI Framework
- SQLite3
- Langchain (for NLP tasks)
- SQLAlchemy (for database operations)

## Future Enhancements
1. Support for multiple database types
2. Query caching and optimization
3. Advanced natural language understanding
4. Interactive query refinement
5. Query explanation generation
6. Additional specialized agents for complex queries
7. Extended tool set for database operations

## Contributing
See the CrewAI documentation for contribution guidelines.

## Support
- [CrewAI Documentation](https://docs.crewai.com/)
- [GitHub Issues](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)

## License
MIT License
