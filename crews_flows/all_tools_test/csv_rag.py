from crewai_tools import CSVSearchTool
import os

csv_search = CSVSearchTool(
    csv="SaleData.csv",
    config=dict(
        llm=dict(
            provider="groq",
            config=dict(
                model="llama3-8b-8192",
                api_key=os.getenv("GROQ_API_KEY"),
            ),
        ),
        embedder=dict(
            provider="huggingface",
            config=dict(
                model="BAAI/bge-small-en-v1.5",
                # document_type="retrieval_document",
            ),
        ),
    ),
)

result = csv_search._run("Home")

print(result)
