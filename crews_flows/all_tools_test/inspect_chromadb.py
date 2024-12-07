import chromadb
from chromadb.config import Settings
import os
import json

def inspect_chromadb(db_path):
    # Initialize ChromaDB client with persistent directory
    client = chromadb.PersistentClient(path=db_path)
    
    # List all collections
    collections = client.list_collections()
    print(f"\nFound {len(collections)} collections:")
    
    for collection in collections:
        print(f"\nCollection: {collection.name}")
        
        # Get all items in the collection
        results = collection.get()
        
        # Print collection statistics
        print(f"Number of documents: {len(results['ids'])}")
        
        # Print document details
        for i in range(len(results['ids'])):
            print(f"\nDocument {i + 1}:")
            print(f"ID: {results['ids'][i]}")
            print(f"Metadata: {json.dumps(results['metadatas'][i], indent=2)}")
            print(f"Document: {results['documents'][i][:200]}...")  # Show first 200 chars
            print("-" * 80)

if __name__ == "__main__":
    # Path to your ChromaDB directory
    db_path = "db/5d113448-18f4-4f22-9e5d-4f1d74fb552f"
    
    try:
        inspect_chromadb(db_path)
    except Exception as e:
        print(f"Error inspecting ChromaDB: {str(e)}")
        
        # Check if directory exists
        if not os.path.exists(db_path):
            print(f"\nDirectory {db_path} does not exist.")
            print("Available directories in 'db':")
            if os.path.exists("db"):
                print("\n".join(os.listdir("db")))
            else:
                print("'db' directory not found")
