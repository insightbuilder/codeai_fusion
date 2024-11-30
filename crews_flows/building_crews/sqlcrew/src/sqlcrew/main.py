#!/usr/bin/env python
import os
import sqlite3
import sys
import warnings
from pathlib import Path

from sqlcrew.crew import Sqlcrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def create_test_database(db_path: str):
    """Create a test database with sample data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Insert sample data
    sample_users = [
        (1, 'John Doe', 'john@example.com'),
        (2, 'Jane Smith', 'jane@example.com'),
        (3, 'Bob Wilson', 'bob@example.com')
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO users (id, name, email) VALUES (?, ?, ?)', sample_users)
    conn.commit()
    conn.close()

def run():
    """Run the SQL Crew with sample database"""
    try:
        # Setup test database
        db_path = Path(__file__).parent / 'database' / 'example.db'
        db_path.parent.mkdir(exist_ok=True)
        create_test_database(str(db_path))
        
        # Define input parameters
        inputs = {
            "nl_query": "How many users are in the database?",
            "schema_info": """
                Table: users
                Columns:
                - id (INTEGER PRIMARY KEY)
                - name (TEXT NOT NULL)
                - email (TEXT UNIQUE NOT NULL)
            """,
            "db_name": str(db_path)
        }
        
        # Run the crew
        result = Sqlcrew().crew().kickoff(inputs=inputs)
        print("\nQuery Result:")
        print("-" * 50)
        print(result)
        
    except Exception as e:
        print(f"\nError running SQL Crew: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run()
