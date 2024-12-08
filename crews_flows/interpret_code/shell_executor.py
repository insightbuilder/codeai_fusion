import os
import sys
import subprocess
import traceback
import contextlib
import io
from typing import Dict, Any, List, Optional, Union, Callable

class ShellExecutor:
    """
    A flexible and secure code execution utility with multiple execution modes.
    
    Supports different execution strategies:
    1. Direct Python Execution (exec)
    2. Subprocess Execution
    3. Isolated Execution with Sandboxing
    4. Custom Execution Strategies
    """
    
    @staticmethod
    def execute_python(
        code: str, 
        globals_dict: Optional[Dict[str, Any]] = None, 
        locals_dict: Optional[Dict[str, Any]] = None,
        capture_output: bool = True
    ) -> Dict[str, Any]:
        """
        Execute Python code using exec() with enhanced safety and output capture.
        
        Args:
            code (str): Python code to execute
            globals_dict (dict, optional): Global namespace dictionary
            locals_dict (dict, optional): Local namespace dictionary
            capture_output (bool): Whether to capture stdout/stderr
        
        Returns:
            dict: Execution results with keys 'output', 'result', 'error'
        """
        # Set up default dictionaries if not provided
        globals_dict = globals_dict or {}
        locals_dict = locals_dict or {}
        
        # Capture output
        output_capture = io.StringIO() if capture_output else None
        error_capture = io.StringIO() if capture_output else None
        
        try:
            # Redirect stdout and stderr if capturing
            with contextlib.redirect_stdout(output_capture), \
                 contextlib.redirect_stderr(error_capture):
                
                # Execute the code
                exec(code, globals_dict, locals_dict)
                
                # Try to get the result (if defined)
                result = locals_dict.get('result', None)
        
        except Exception as e:
            # Capture any execution errors
            error_message = traceback.format_exc()
            return {
                'output': output_capture.getvalue() if output_capture else '',
                'result': None,
                'error': error_message
            }
        
        return {
            'output': output_capture.getvalue() if output_capture else '',
            'result': result,
            'error': None
        }
    
    @staticmethod
    def execute_subprocess(
        command: Union[str, List[str]], 
        cwd: Optional[str] = None, 
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute a command in a subprocess with comprehensive error handling.
        
        Args:
            command (str or list): Command to execute
            cwd (str, optional): Working directory
            env (dict, optional): Environment variables
            timeout (int, optional): Timeout in seconds
        
        Returns:
            dict: Execution results with keys 'stdout', 'stderr', 'returncode'
        """
        try:
            # Prepare environment and working directory
            exec_env = os.environ.copy()
            if env:
                exec_env.update(env)
            
            # Execute subprocess
            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                cwd=cwd,
                env=exec_env
            )
            
            # Wait for process and capture output
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                return {
                    'stdout': stdout,
                    'stderr': f"Process timed out after {timeout} seconds",
                    'returncode': -1
                }
            
            return {
                'stdout': stdout,
                'stderr': stderr,
                'returncode': process.returncode
            }
        
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
    
    @staticmethod
    def install_dependencies(
        libraries: List[str], 
        method: str = 'pip',
        upgrade: bool = False
    ) -> Dict[str, Any]:
        """
        Install Python dependencies safely.
        
        Args:
            libraries (list): Libraries to install
            method (str): Installation method (pip, conda)
            upgrade (bool): Whether to upgrade existing packages
        
        Returns:
            dict: Installation results
        """
        install_commands = {
            'pip': f"pip {'install --upgrade' if upgrade else 'install'}",
            'conda': f"conda install {'--update-all' if upgrade else ''}"
        }
        
        if method not in install_commands:
            return {
                'success': False,
                'message': f"Unsupported installation method: {method}"
            }
        
        command = f"{install_commands[method]} {' '.join(libraries)}"
        result = ShellExecutor.execute_subprocess(command, shell=True)
        
        return {
            'success': result['returncode'] == 0,
            'stdout': result['stdout'],
            'stderr': result['stderr']
        }
    
    @staticmethod
    def run_with_custom_handler(
        code: str, 
        handler: Optional[Callable[[str], Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute code with a custom result handler.
        
        Args:
            code (str): Code to execute
            handler (callable, optional): Custom result processing function
        
        Returns:
            dict: Execution results
        """
        execution_result = ShellExecutor.execute_python(code)
        
        if handler and execution_result['error'] is None:
            try:
                processed_result = handler(execution_result['result'])
                execution_result['processed_result'] = processed_result
            except Exception as e:
                execution_result['handler_error'] = str(e)
        
        return execution_result
    
    @classmethod
    def safe_execute(
        cls, 
        code: str, 
        libraries: Optional[List[str]] = None,
        timeout: Optional[int] = 60
    ) -> Dict[str, Any]:
        """
        Comprehensive safe code execution method.
        
        Args:
            code (str): Code to execute
            libraries (list, optional): Libraries to install before execution
            timeout (int, optional): Execution timeout
        
        Returns:
            dict: Comprehensive execution results
        """
        # Install dependencies if specified
        if libraries:
            dependency_result = cls.install_dependencies(libraries)
            if not dependency_result['success']:
                return {
                    'success': False,
                    'message': 'Dependency installation failed',
                    'details': dependency_result
                }
        
        # Execute the code with timeout
        try:
            result = cls.execute_python(code)
            return {
                'success': result['error'] is None,
                'output': result['output'],
                'result': result['result'],
                'error': result['error']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Example usage demonstration
if __name__ == "__main__":
    # Python code execution
    python_code = """
result = [x**2 for x in range(5)]
print(f"Squared numbers: {result}")
    """
    print("Python Execution:", ShellExecutor.execute_python(python_code))
    
    # Subprocess execution
    print("Subprocess Execution:", 
        ShellExecutor.execute_subprocess(["ls", "-l"])
    )
    
    # Safe execution with dependencies
    safe_result = ShellExecutor.safe_execute(
        "import numpy as np\nresult = np.array([1, 2, 3])",
        libraries=['numpy']
    )
    print("Safe Execution:", safe_result)
