# shell_executor_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Type, Optional
import os
import subprocess

class ShellExecutorSchema(BaseModel):
    """Input schema for ShellExecutorTool."""

    command: str = Field(
        ..., 
        description="Shell command to be executed. Can be a single command or a complex shell script."
    )

    working_directory: Optional[str] = Field(
        default=None, 
        description="Optional working directory for command execution. If not specified, uses current directory."
    )

    environment_vars: Optional[Dict[str, str]] = Field(
        default=None, 
        description="Optional environment variables to set for the command execution."
    )

    timeout: Optional[int] = Field(
        default=60, 
        description="Timeout for command execution in seconds. Default is 60 seconds."
    )


class ShellExecutorTool(BaseTool):
    """
    A CrewAI tool for executing shell commands with enhanced safety and flexibility.
    
    Features:
    - Secure shell command execution
    - Configurable working directory
    - Environment variable support
    - Timeout management
    """
    
    name: str = "Shell Executor"
    description: str = "Executes shell commands with enhanced safety and flexibility."
    args_schema: Type[BaseModel] = ShellExecutorSchema

    def _run(
        self, 
        command: str, 
        working_directory: Optional[str] = None, 
        environment_vars: Optional[Dict[str, str]] = None, 
        timeout: int = 60
    ) -> str:
        """
        Execute a shell command with comprehensive error handling and configuration.
        
        Args:
            command (str): Shell command to execute
            working_directory (str, optional): Directory to run the command in
            environment_vars (dict, optional): Environment variables to set
            timeout (int, optional): Maximum execution time in seconds
        
        Returns:
            str: Command execution result or error message
        """
        try:
            # Prepare environment variables
            exec_env = os.environ.copy()
            if environment_vars:
                exec_env.update(environment_vars)
            
            # Set working directory (default to current directory)
            cwd = working_directory or os.getcwd()
            
            # Execute subprocess with comprehensive configuration
            try:
                process = subprocess.Popen(
                    command, 
                    shell=True,  # Allow complex shell commands
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=cwd,
                    env=exec_env
                )
                
                # Wait for process with timeout
                try:
                    stdout, stderr = process.communicate(timeout=timeout)
                    
                    # Check return code
                    if process.returncode == 0:
                        return stdout.strip() or "Command executed successfully."
                    else:
                        return f"Command failed with return code {process.returncode}. Error: {stderr}"
                
                except subprocess.TimeoutExpired:
                    process.kill()
                    return f"Command timed out after {timeout} seconds."
            
            except Exception as exec_error:
                return f"Execution error: {str(exec_error)}"
        
        except Exception as setup_error:
            return f"Setup error: {str(setup_error)}"


# Optional: Demonstration of tool usage
if __name__ == "__main__":
    # Example usage
    shell_tool = ShellExecutorTool()
    
    # List files in current directory
    print(shell_tool._run("ls -l"))
    
    # Run a Python script with custom working directory
    print(shell_tool._run(
        "python -c 'print(\"Hello from subprocess!\")'", 
        working_directory="/tmp"
    ))
    
    # Execute with environment variables
    print(shell_tool._run(
        "echo $CUSTOM_VAR", 
        environment_vars={"CUSTOM_VAR": "subprocess test"}
    ))
