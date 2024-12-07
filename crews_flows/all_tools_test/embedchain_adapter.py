from typing import Any

from embedchain import App

from crewai_tools.tools.rag.rag_tool import Adapter


class EmbedchainAdapter(Adapter):
    embedchain_app: App
    summarize: bool = False

    def query(self, question: str) -> str:
        try:
            result, sources = self.embedchain_app.query(
                question, citations=True, dry_run=False  # Changed to always get results
            )
            
            # Always return both result and sources for better context
            if result and sources:
                formatted_sources = "\n\n".join([source[0] for source in sources])
                return f"{result}\n\nSources:\n{formatted_sources}"
            elif result:
                return result
            elif sources:
                return "\n\n".join([source[0] for source in sources])
            else:
                return "No relevant information found."
                
        except Exception as e:
            return f"Error during query: {str(e)}"

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        try:
            self.embedchain_app.add(*args, **kwargs)
        except Exception as e:
            print(f"Error adding content: {str(e)}")
            raise
