from crewai_tools import CodeDocsSearchTool
import os

doc_search = CodeDocsSearchTool(
    docs_url="https://docs.crewai.com/",
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

tools_rag = doc_search._run("List the RAG Tools in CreWAI Tools")

print(tools_rag)
