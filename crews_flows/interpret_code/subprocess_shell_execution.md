# Subprocess Shell Execution Guide

## Overview

Subprocess shell execution is a powerful technique for running system commands, scripts, and external programs from within Python. The `ShellExecutor` provides a robust and flexible approach to executing shell commands safely and efficiently.

## Key Concepts

### What is Subprocess Execution?
Subprocess execution allows you to:
- Run system commands
- Execute shell scripts
- Interact with external programs
- Capture command output
- Manage command execution environment

## ShellExecutor Subprocess Methods

### 1. Basic Subprocess Execution

```python
from shell_executor import ShellExecutor

# Execute a simple command
result = ShellExecutor.execute_subprocess(["ls", "-l"])
```

#### Result Structure
```python
{
    'stdout': '... command output ...',  # Standard output
    'stderr': '... error messages ...',  # Standard error
    'returncode': 0  # Command exit status
}
```

### 2. Advanced Subprocess Execution

```python
# Execute with custom working directory and environment
result = ShellExecutor.execute_subprocess(
    command="python script.py",
    cwd="/path/to/project",
    env={"CUSTOM_VAR": "value"},
    timeout=30  # 30-second timeout
)
```

## Execution Strategies

### Command Types
1. **List Commands**: Recommended for most scenarios
   ```python
   ShellExecutor.execute_subprocess(["git", "clone", "https://github.com/example/repo"])
   ```

2. **String Commands**: Use with caution, requires `shell=True`
   ```python
   ShellExecutor.execute_subprocess(
       "pip install numpy && python -c 'import numpy'", 
       shell=True
   )
   ```

### Error Handling

```python
result = ShellExecutor.execute_subprocess(["command"])
if result['returncode'] != 0:
    print(f"Error occurred: {result['stderr']}")
```

## Best Practices

### Security Considerations
- Avoid using `shell=True` with untrusted input
- Sanitize and validate command arguments
- Use list-based commands when possible

### Performance Tips
- Use timeouts to prevent hanging
- Capture output to avoid blocking
- Close file descriptors after use

## Common Use Cases

### 1. Package Management
```python
# Install Python packages
ShellExecutor.execute_subprocess(["pip", "install", "requests"])
```

### 2. Git Operations
```python
# Clone a repository
ShellExecutor.execute_subprocess([
    "git", "clone", "https://github.com/user/repo.git"
])
```

### 3. System Information
```python
# Get system information
system_info = ShellExecutor.execute_subprocess(["uname", "-a"])
```

## Advanced Techniques

### Dependency Installation
```python
# Install multiple libraries
dependencies = ['numpy', 'pandas', 'matplotlib']
ShellExecutor.install_dependencies(dependencies)
```

### Custom Execution Handler
```python
def process_result(result):
    # Custom result processing logic
    return result.upper()

custom_result = ShellExecutor.run_with_custom_handler(
    "print('hello world')", 
    handler=process_result
)
```

## Troubleshooting

### Common Issues
- **Permission Denied**: Ensure proper file permissions
- **Timeout Errors**: Adjust timeout for long-running commands
- **Environment Conflicts**: Verify environment variables

### Debugging Techniques
```python
# Verbose subprocess execution
result = ShellExecutor.execute_subprocess(
    ["your_command"],
    capture_output=True  # Capture detailed output
)
print(result['stdout'])
print(result['stderr'])
```

## Error Handling Patterns

```python
def safe_command_execution(command):
    try:
        result = ShellExecutor.execute_subprocess(command)
        if result['returncode'] == 0:
            return result['stdout']
        else:
            print(f"Command failed: {result['stderr']}")
    except Exception as e:
        print(f"Execution error: {e}")
```

## Performance Monitoring

- Use `timeout` to prevent indefinite execution
- Capture both stdout and stderr
- Check return codes for command success

## Conclusion

The `ShellExecutor` provides a comprehensive, safe, and flexible approach to subprocess shell execution in Python. By following best practices and understanding its capabilities, you can effectively interact with system commands and external programs.

### Recommended Reading
- Python `subprocess` module documentation
- Security guidelines for shell command execution
- System administration best practices

## References
- Python Official Documentation
- subprocess module
- Shell scripting best practices

## Python `exec()` Function: Dynamic Code Execution

### What is `exec()`?

The `exec()` function is a powerful Python built-in that allows dynamic execution of Python code represented as a string. It provides a way to run code generated at runtime, enabling metaprogramming and dynamic code generation.

### Basic Syntax

```python
exec(object[, globals[, locals]])
```

- `object`: A string or code object to be executed
- `globals`: Optional dictionary representing global namespace
- `locals`: Optional dictionary representing local namespace

### Execution Modes

#### 1. Simple Execution
```python
# Execute a simple Python statement
exec("x = 10")
print(x)  # Outputs: 10
```

#### 2. Multiple Statements
```python
# Execute multiple statements
exec("""
def greet(name):
    return f"Hello, {name}!"

result = greet('World')
print(result)
""")
```

### Namespace Management

#### Isolated Namespace
```python
# Create an isolated namespace
global_namespace = {}
local_namespace = {}

exec("""
x = 100
y = 200
def calculate():
    return x + y
""", global_namespace, local_namespace)

# Access variables from the isolated namespace
print(local_namespace['x'])  # 100
print(local_namespace['calculate']())  # 300
```

### Advanced Usage

#### Dynamic Function Creation
```python
def create_function(func_body):
    namespace = {}
    exec(f"""
def dynamic_func():
{func_body}
""", namespace)
    return namespace['dynamic_func']

# Create a function dynamically
printer = create_function("    print('Hello from dynamic function!')")
printer()  # Outputs: Hello from dynamic function!
```

### Safety and Security Considerations

#### Potential Risks
- Executing untrusted code can be dangerous
- Can potentially access system resources
- Bypasses normal import and module mechanisms

#### Safe Execution Patterns
```python
def safe_exec(code_string, timeout=5):
    try:
        # Limit global and local namespaces
        global_ns = {'__builtins__': {}}
        local_ns = {}
        
        # Set a timeout for execution
        import signal
        
        def handler(signum, frame):
            raise TimeoutError("Code execution timed out")
        
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)
        
        try:
            exec(code_string, global_ns, local_ns)
        finally:
            signal.alarm(0)  # Disable the alarm
        
        return local_ns.get('result')
    
    except Exception as e:
        print(f"Execution error: {e}")
        return None
```

### Performance Considerations

- `exec()` is slower compared to compiled code
- Creates overhead for code parsing and execution
- Not recommended for performance-critical sections

### Use Cases

1. **Configuration Parsing**
```python
config = """
database = {
    'host': 'localhost',
    'port': 5432,
    'username': 'admin'
}
"""
namespace = {}
exec(config, namespace)
print(namespace['database'])
```

2. **Dynamic Plugin Systems**
```python
def load_plugin(plugin_code):
    namespace = {}
    exec(plugin_code, namespace)
    return namespace.get('Plugin')

# Dynamically load a plugin
plugin_code = """
class Plugin:
    def process(self, data):
        return data.upper()
"""
plugin_class = load_plugin(plugin_code)
```

### Limitations and Alternatives

- Use `ast.literal_eval()` for safer expression evaluation
- Consider `importlib` for dynamic module loading
- Use compilation techniques for complex scenarios

### Best Practices

1. Never execute untrusted code
2. Use isolated namespaces
3. Implement strict input validation
4. Consider alternatives when possible
5. Add timeouts and resource limits

### Error Handling

```python
def robust_exec(code, max_lines=10):
    try:
        # Prevent overly large code execution
        if len(code.splitlines()) > max_lines:
            raise ValueError("Code exceeds maximum allowed lines")
        
        # Capture output
        import io
        import sys
        
        output_capture = io.StringIO()
        sys.stdout = output_capture
        
        exec(code)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        return output_capture.getvalue()
    
    except Exception as e:
        return f"Execution failed: {e}"
```

### Conclusion

The `exec()` function is a powerful tool for dynamic code execution, offering flexibility in metaprogramming. However, it should be used with extreme caution, implementing robust safety mechanisms to prevent potential security risks.

## CrewAI ShellExecutorTool: Advanced Shell Command Execution

### Overview

The `ShellExecutorTool` is a specialized CrewAI tool designed for secure and flexible shell command execution within AI-driven workflows. It provides a robust interface for running shell commands with enhanced safety, configuration, and error handling.

### Tool Architecture

```python
class ShellExecutorTool(BaseTool):
    name = "Shell Executor"
    description = "Executes shell commands with enhanced safety and flexibility."
```

### Input Schema

The tool uses a Pydantic schema to validate and configure command execution:

```python
class ShellExecutorSchema(BaseModel):
    command: str  # Required shell command
    working_directory: Optional[str]  # Optional execution directory
    environment_vars: Optional[Dict[str, str]]  # Custom environment variables
    timeout: Optional[int] = 60  # Command execution timeout
```

### Execution Capabilities

#### 1. Basic Command Execution
```python
shell_tool = ShellExecutorTool()
result = shell_tool._run("ls -l")  # List directory contents
```

#### 2. Advanced Configuration
```python
# Execute with custom working directory
result = shell_tool._run(
    command="python script.py", 
    working_directory="/path/to/project"
)

# Set environment variables
result = shell_tool._run(
    command="echo $API_KEY", 
    environment_vars={"API_KEY": "secret_key"}
)
```

### Key Features

1. **Secure Execution**
   - Isolated command execution
   - Environment variable management
   - Working directory configuration

2. **Error Handling**
   - Comprehensive error capturing
   - Timeout management
   - Return code validation

3. **Flexible Configuration**
   - Support for complex shell commands
   - Dynamic environment setup
   - Configurable execution context

### Error Handling Mechanisms

```python
def _run(self, command, working_directory=None, environment_vars=None, timeout=60):
    try:
        # Prepare execution environment
        exec_env = os.environ.copy()
        if environment_vars:
            exec_env.update(environment_vars)
        
        # Execute subprocess
        process = subprocess.Popen(
            command, 
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            cwd=working_directory or os.getcwd(),
            env=exec_env
        )
        
        # Handle timeout and output
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            
            if process.returncode == 0:
                return stdout.strip()
            else:
                return f"Command failed: {stderr}"
        
        except subprocess.TimeoutExpired:
            process.kill()
            return f"Command timed out after {timeout} seconds"
    
    except Exception as e:
        return f"Execution error: {str(e)}"
```

### Use Cases

1. **System Automation**
   - Running system scripts
   - Executing maintenance tasks
   - Retrieving system information

2. **Development Workflows**
   - Running build scripts
   - Deploying applications
   - Managing development environments

3. **Data Processing**
   - Executing data transformation scripts
   - Running batch processing jobs
   - Interacting with system utilities

### Best Practices

1. **Security**
   - Validate and sanitize input commands
   - Use minimal required permissions
   - Avoid executing untrusted commands

2. **Performance**
   - Set appropriate timeouts
   - Monitor resource consumption
   - Use efficient command implementations

3. **Error Management**
   - Always handle potential errors
   - Log command execution details
   - Implement retry mechanisms

### Integration with CrewAI

```python
from crewai import Agent, Task, Crew

# Create an agent with shell execution capabilities
system_admin = Agent(
    role="System Administrator",
    goal="Automate system tasks",
    tools=[ShellExecutorTool()]
)

# Define a task using shell execution
system_check_task = Task(
    description="Perform system health check",
    agent=system_admin,
    tool=ShellExecutorTool()
)
```

### Limitations and Considerations

- Not suitable for interactive commands
- Potential security risks with untrusted input
- Performance overhead for complex commands
- Platform-dependent behavior

### Conclusion

The `ShellExecutorTool` provides a powerful, flexible, and secure method for executing shell commands within CrewAI workflows, enabling complex system interactions while maintaining robust error handling and configuration options.
