from crewai_tools import PDFSearchTool
import os

# Initialize the PDFSearchTool with the correct configuration
rag_tool = PDFSearchTool(
    pdf="9.pdf",  # PDF file exists in the current directory
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
            ),
        ),
    ),
)

try:
    # Run the query
    out_rag = rag_tool.run("How does exercise price work?")
    print("RAG Tool Output:", out_rag)
except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    traceback.print_exc()
