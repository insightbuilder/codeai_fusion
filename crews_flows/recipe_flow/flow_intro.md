# Integrating CrewAI Crews with CrewAI Flows

This guide explains how to integrate CrewAI Crews with CrewAI Flows to create powerful, orchestrated AI workflows.

## Overview

CrewAI Flows extend the capabilities of CrewAI Crews by providing:
- Structured workflow management
- State handling between crew interactions
- Enhanced error handling and recovery
- Better orchestration of multiple crews

## Integration Steps

### 1. Define Your Flow Class

```python
from crewai_flows import Flow
from typing import Dict, Any

class MyCustomFlow(Flow):
    def __init__(self):
        super().__init__()
        self.state = {}  # Initialize flow state

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation of your flow logic
        pass
```

### 2. Create Your Crew

```python
from crewai import Crew, Agent, Task

# Define your agents
researcher = Agent(
    role='Researcher',
    goal='Conduct thorough research on the topic',
    backstory='Expert research analyst with vast experience'
)

writer = Agent(
    role='Writer',
    goal='Create compelling content based on research',
    backstory='Professional content writer with expertise in technical writing'
)

# Create tasks
research_task = Task(
    description='Research the given topic thoroughly',
    agent=researcher
)

writing_task = Task(
    description='Write content based on research findings',
    agent=writer
)

# Initialize your crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task]
)
```

### 3. Integrate Crew with Flow

```python
class ContentCreationFlow(Flow):
    def __init__(self):
        super().__init__()
        self.state = {
            'research_results': None,
            'final_content': None
        }

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Initialize crew
        crew = self._create_crew()
        
        # Execute crew tasks
        result = await crew.kickoff()
        
        # Update flow state
        self.state['final_content'] = result
        
        return self.state

    def _create_crew(self):
        # Crew creation logic here
        pass
```

### 4. Execute the Flow

```python
async def main():
    # Initialize your flow
    flow = ContentCreationFlow()
    
    # Prepare input data
    input_data = {
        'topic': 'AI and Machine Learning',
        'requirements': 'Technical but accessible content'
    }
    
    # Run the flow
    result = await flow.run(input_data)
    print(result)

# Run the flow
import asyncio
asyncio.run(main())
```

## Best Practices

1. **State Management**
   - Keep track of important data in the flow's state
   - Use type hints for better code clarity
   - Handle state persistence if needed

2. **Error Handling**
   ```python
   async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
       try:
           result = await self._execute_crew_tasks()
           return result
       except Exception as e:
           self.handle_error(e)
           raise
   ```

3. **Flow Configuration**
   - Use configuration files for flow settings
   - Implement environment variable support
   - Keep sensitive data secure

4. **Monitoring and Logging**
   - Implement proper logging
   - Add monitoring points
   - Track flow metrics

## Advanced Features

### Parallel Execution
```python
async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    tasks = []
    for crew in self.crews:
        tasks.append(crew.kickoff())
    
    results = await asyncio.gather(*tasks)
    return self._process_results(results)
```

### State Persistence
```python
class PersistentFlow(Flow):
    async def save_state(self):
        # Save flow state to database/file
        pass

    async def load_state(self):
        # Load flow state from database/file
        pass
```

## Conclusion

Integrating CrewAI Crews with CrewAI Flows provides a robust framework for building complex AI workflows. This integration allows for better organization, state management, and execution control of your AI crews.

Remember to:
- Keep your flows modular and reusable
- Implement proper error handling
- Maintain clear state management
- Follow async/await patterns consistently
- Add appropriate logging and monitoring

For more examples and detailed documentation, refer to the official CrewAI documentation.
