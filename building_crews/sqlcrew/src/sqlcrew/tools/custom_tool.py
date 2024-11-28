from crewai_tools import tool
import sqlite3


@tool
def translate_to_sql(nl_query: str, schema_info: str) -> str:
    """
    Translate a natural language query into a SQL statement using the provided schema information.
    
    Args:
        nl_query: Natural language query from the user
        schema_info: Database schema information including tables and columns
        
    Returns:
        str: Generated SQL query or error message
    """
    # This is a simple mapping for demonstration. In a real implementation,
    # you would use an LLM to generate the SQL query based on the schema
    sql_map = {
        "How many users are in the database?": "SELECT COUNT(*) as user_count FROM users;",
        "What is the email of John Doe?": "SELECT email FROM users WHERE name = 'John Doe';",
        "List all users": "SELECT * FROM users;",
    }
    return sql_map.get(nl_query, "Unable to process query. Please rephrase.")


@tool
def execute_sql(db_name: str, query: str) -> str:
    """
    Execute the SQL query on the database and return the results.
    
    Args:
        db_name: Name of the SQLite database file
        query: SQL query to execute
        
    Returns:
        str: Query results or error message
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names from cursor description
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            
            # Format results as a list of dictionaries
            formatted_results = []
            for row in results:
                formatted_results.append(dict(zip(columns, row)))
            
            return f"Results: {formatted_results}" if formatted_results else "No results found"
        return "Query executed successfully (no results to return)"
    
    except Exception as e:
        return f"Error executing query: {str(e)}"
    finally:
        if 'conn' in locals():
            conn.close()
