# tools/code_interpreter.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List, Type
import os


class CodeInterpreterSchema(BaseModel):
    """Input for CodeInterpreterTool."""

    code: str = Field(
        ...,
        description="Python3 code used to be interpreted in the Docker container. ALWAYS PRINT the final result and the output of the code",
    )

    libraries_used: List[str] = Field(
        ...,
        description="List of libraries used in the code with proper installing names separated by commas. Example: numpy,pandas,beautifulsoup4",
    )


class CodeInterpreterTool(BaseTool):
    name: str = "Code Interpreter"
    description: str = "Interprets Python3 code strings with a final print statement."
    args_schema: Type[BaseModel] = CodeInterpreterSchema

    def _run(self, code: str, libraries_used: List[str]) -> str:
        """
        Run the code directly on the host machine (unsafe mode).
        """
        # Install libraries on the host machine
        for library in libraries_used:
            os.system(f"pip install {library}")

        # Execute the code
        try:
            exec_locals = {}
            exec(code, {}, exec_locals)
            return exec_locals.get("result", "No result variable found.")
        except Exception as e:
            return f"An error occurred: {str(e)}"
