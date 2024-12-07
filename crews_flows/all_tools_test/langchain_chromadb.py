from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
import os

def create_langchain_chromadb(csv_path, persist_directory="langchain_db"):
    # Initialize the embedding model (same as in your current setup)
    model_name = "BAAI/bge-small-en-v1.5"
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        encode_kwargs=encode_kwargs
    )
    
    # Load and prepare the CSV data
    df = pd.read_csv(csv_path)
    
    # Convert DataFrame to text documents
    documents = []
    for idx, row in df.iterrows():
        # Convert each row to a string representation
        doc = " ".join([f"{col}: {val}" for col, val in row.items()])
        documents.append(doc)
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.create_documents(documents)
    
    # Create and persist the vector store
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    return vectordb

def query_langchain_chromadb(query, persist_directory="langchain_db"):
    # Initialize the embedding model
    model_name = "BAAI/bge-small-en-v1.5"
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        encode_kwargs=encode_kwargs
    )
    
    # Load the existing vector store
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    # Perform similarity search
    results = vectordb.similarity_search_with_relevance_scores(query, k=3)
    
    print(f"\nQuery: {query}")
    print("\nResults:")
    for doc, score in results:
        print(f"\nRelevance Score: {score:.4f}")
        print(f"Content: {doc.page_content}")
        print("-" * 80)

if __name__ == "__main__":
    csv_path = "SaleData.csv"
    persist_dir = "langchain_db"
    
    # Create new vector store if it doesn't exist
    if not os.path.exists(persist_dir):
        print("Creating new vector store...")
        vectordb = create_langchain_chromadb(csv_path, persist_dir)
        print("Vector store created and persisted.")
    
    # Example queries
    queries = [
        "Show me information about Home products",
        "What are the total sales?",
        "Show me orders with high quantities"
    ]
    
    for query in queries:
        query_langchain_chromadb(query, persist_dir)
