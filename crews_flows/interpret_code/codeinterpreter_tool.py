# tools/code_interpreter.py
from crewai.tools import tool


@tool
def code_interpreter(code: str) -> str:
    """
    Execute the given Python code and return the output.

    Args:
        code (str): The Python code to execute.

    Returns:
        str: Output of the executed code.
    """
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return str(exec_globals.get("result", "Code executed successfully."))
    except Exception as e:
        return str(e)
