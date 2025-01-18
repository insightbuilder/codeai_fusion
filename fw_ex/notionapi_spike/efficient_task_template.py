import os
from notion_client import Client
from typing import Dict, Any
from datetime import datetime
from rich import print

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
client = Client(auth=NOTION_TOKEN)

# pyright: reportIndexIssue=false


def create_database_schema() -> Dict[str, Any]:
    """Define the database schema for efficient task management"""
    return {
        "title": [{"type": "text", "text": {"content": "Efficient Task Management"}}],
        "properties": {
            "Task Name": {"title": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Not Started", "color": "red"},
                        {"name": "In Progress", "color": "yellow"},
                        {"name": "Waiting", "color": "orange"},
                        {"name": "Completed", "color": "green"},
                        {"name": "Cancelled", "color": "gray"},
                    ]
                }
            },
            "Priority": {
                "select": {
                    "options": [
                        {"name": "High", "color": "red"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "Low", "color": "blue"},
                    ]
                }
            },
            "Due Date": {"date": {}},
            "Category": {
                "multi_select": {
                    "options": [
                        {"name": "Work", "color": "blue"},
                        {"name": "Personal", "color": "green"},
                        {"name": "Health", "color": "red"},
                        {"name": "Learning", "color": "purple"},
                        {"name": "Finance", "color": "yellow"},
                    ]
                }
            },
            "Effort": {
                "select": {
                    "options": [
                        {"name": "Quick Win", "color": "green"},
                        {"name": "Med   ium", "color": "yellow"},
                        {"name": "Major Project", "color": "red"},
                    ]
                }
            },
            "Progress": {"number": {"format": "percent"}},
            "Assigned To": {"people": {}},
            # "Related Tasks": {"relation": {}},
            "Notes": {"rich_text": {}},
            "Created Date": {"created_time": {}},
            "Last Modified": {"last_edited_time": {}},
        },
    }


def create_sample_tasks(database_id: str) -> None:
    """Create sample tasks to demonstrate database usage"""
    sample_tasks = [
        {
            "Task Name": {"title": [{"text": {"content": "Set up project planning"}}]},
            "Status": {"select": {"name": "Not Started"}},
            "Priority": {"select": {"name": "High"}},
            "Due Date": {"date": {"start": datetime.now().isoformat()}},
            "Category": {"multi_select": [{"name": "Work"}]},
            "Effort": {"select": {"name": "Medium"}},
            "Progress": {"number": 0},
            "Notes": {
                "rich_text": [
                    {"text": {"content": "Initial project setup and planning phase"}}
                ]
            },
        },
        {
            "Task Name": {"title": [{"text": {"content": "Daily Exercise Routine"}}]},
            "Status": {"select": {"name": "In Progress"}},
            "Priority": {"select": {"name": "Medium"}},
            "Due Date": {"date": {"start": datetime.now().isoformat()}},
            "Category": {"multi_select": [{"name": "Health"}, {"name": "Personal"}]},
            "Effort": {"select": {"name": "Quick Win"}},
            "Progress": {"number": 50},
            "Notes": {
                "rich_text": [{"text": {"content": "30 minutes of daily exercise"}}]
            },
        },
    ]

    for task in sample_tasks:
        client.pages.create(parent={"database_id": database_id}, properties=task)


def main():
    try:
        # Create the database
        response = client.databases.create(
            parent={
                "type": "page_id",
                "page_id": "17f84ade96ac8053b275c0ea5e381ec4",
            },  # Replace with your page ID
            **create_database_schema(),
        )

        database_id = response["id"]
        print(f"✅ Database created successfully with ID: {database_id}")

        # Create sample tasks
        create_sample_tasks(database_id)
        print("✅ Sample tasks created successfully")

        print("\nDatabase Views:")
        print("1. List View: Sort by Priority and Due Date")
        print("2. Board View: Group by Status")
        print("3. Calendar View: Organized by Due Date")
        print("4. Gallery View: Visual task cards")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()

