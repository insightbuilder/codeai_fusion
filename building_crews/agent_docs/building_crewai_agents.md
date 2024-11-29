---
id: 1732781779-BBNY
aliases:
  - process of creating crew, agents, and flows
tags: []
---

# process of creating crew, agents, and flows

Development Guidelines:

- Install the pre-requisites with below command

```
python -m venv crewenv
source crewenv/bin/activate
pip install crewai crewai-tools
```

- Create your first crew with below command

```
crewai create crew your_crew
```

The above command would have created the project
structure with the files and folders. Our task
will be update the below files based on the
overall that we are trying to achieve

```
Modify src/my_project/config/agents.yaml to define your agents.
Modify src/my_project/config/tasks.yaml to define your tasks.

You can also modify the agents as needed to fit
your use case or copy and paste as is to your
project.
Any variable interpolated in your agents.yaml and
tasks.yaml files like {topic} will be replaced
by the value of the variable in the main.py file.


After modifying the agents.yaml and tasks.yaml, our next
step is to update the crew.py, to create the
crew in memory for executiona.

Modify src/my_project/crew.py to add your own logic, tools, and specific arguments.
Modify src/my_project/main.py to add custom inputs for your agents and tasks.
crew.py contains the main logic, running crew.
In the main.py user inputs can be provided.
Logic is only kept in crew.py


Add your environment variables into the .env file.
This file contains the OPENAI_API_KEY, and SERPAPI_API_KEY.
```

- Next we run the crew with

```
crew run
```

This will run the installation of supporting
packages inside a venv that is managed by poetry.
Using the packages inside it, it will run the
crew.

### Agents & Tasks yaml configuration

- Note how we use the same name for the agent in
  the agents.yaml (email_summarizer) file as the
  method name in the crew.py (email_summarizer)
  file.

```
email_summarizer:
    role: >
      Email Summarizer
    goal: >
      Summarize emails into a concise and clear summary
    backstory: >
      You will create a 5 bullet point summary of the report
    llm: mixtal_llm

```

- Note how we use the same name for the agent in
  the tasks.yaml (email_summarizer_task) file as
  the method name in the crew.py
  (email_summarizer_task) file.

```

email_summarizer_task:
    description: >
      Summarize the email into a 5 bullet point summary
    expected_output: >
      A 5 bullet point summary of the email
    agent: email_summarizer
    context:
      - reporting_task
      - research_task
```

- subsequently these tasks and agents get called
  inside crew.py

```
# ...
@agent
def email_summarizer(self) -> Agent:
    return Agent(
        config=self.agents_config["email_summarizer"],
    )

@task
def email_summarizer_task(self) -> Task:
    return Task(
        config=self.tasks_config["email_summarizer_task"],
    )
# ...
```

The agents have the topic and the tasks, along
with the tools

While the tasks has the agent, the type of output.
and the task detail description. Tasks also can
have tools. They are not different from what
agents have.

Specifying tools in a task allows for dynamic
adaptation of agent capabilities, emphasizing
CrewAI’s flexibility.

## Creating Agents & Tasks

An agent is an autonomous unit programmed to:

Perform tasks

Make decisions

Communicate with other agents

Think of an agent as a member of a team, with
specific skills and a particular job to do. Agents
can have different roles like Researcher, Writer,
or Customer Support, each contributing to the
overall goal of the crew.

```
from crewai import Agent

agent = Agent(
  role='Data Analyst',
  goal='Extract actionable insights',
  backstory="""You're a data analyst at a large company.
    You're responsible for analyzing data and providing insights
    to the business.
    You're currently working on a project to analyze the
    performance of our marketing campaigns.""",
  tools=[my_tool1, my_tool2],  # Optional, defaults to an empty list
  llm=my_llm,  # Optional
  function_calling_llm=my_llm,  # Optional
  max_iter=15,  # Optional
  max_rpm=None, # Optional
  max_execution_time=None, # Optional
  verbose=True,  # Optional
  allow_delegation=False,  # Optional
  step_callback=my_intermediate_step_callback,  # Optional
  cache=True,  # Optional
  system_template=my_system_template,  # Optional
  prompt_template=my_prompt_template,  # Optional
  response_template=my_response_template,  # Optional
  config=my_config,  # Optional
  crew=my_crew,  # Optional
  tools_handler=my_tools_handler,  # Optional
  cache_handler=my_cache_handler,  # Optional
  callbacks=[callback1, callback2],  # Optional
  allow_code_execution=True,  # Optional
  max_retry_limit=2,  # Optional
  use_system_prompt=True,  # Optional
  respect_context_window=True,  # Optional
  code_execution_mode='safe',  # Optional, defaults to 'safe'
)

```

Next is tasks

Detailed guide on managing and creating tasks
within the CrewAI framework, reflecting the latest
codebase updates.

In the CrewAI framework, a Task is a specific
assignment completed by an Agent.

They provide all necessary details for execution,
such as a description, the agent responsible,
required tools, and more, facilitating a wide
range of action complexities.

Tasks within CrewAI can be collaborative,
requiring multiple agents to work together. This
is managed through the task properties and
orchestrated by the Crew’s process, enhancing
teamwork and efficiency.

Creating a Task:

```
from crewai import Task

task = Task(
    description='Find and summarize the latest and most relevant news on AI',
    agent=sales_agent,
    expected_output='A bullet list summary of the top 5 most important AI news',
)

```

Directly specify an agent for assignment or let
the hierarchical CrewAI’s process decide based on
roles, availability, etc.

By default, the TaskOutput will only include the
raw output. A TaskOutput will only include the
pydantic or json_dict output if the original Task
object was configured with output_pydantic or
output_json, respectively.

Lets see example of Tasks with Tools

```
import os
os.environ["OPENAI_API_KEY"] = "Your Key"
os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

research_agent = Agent(
  role='Researcher',
  goal='Find and summarize the latest AI news',
  backstory="""You're a researcher at a large company.
  You're responsible for analyzing data and providing insights
  to the business.""",
  verbose=True
)

# to perform a semantic search for a specified query from a text's content across the internet
search_tool = SerperDevTool()

task = Task(
  description='Find and summarize the latest AI news',
  expected_output='A bullet list summary of the top 5 most important AI news',
  agent=research_agent,
  tools=[search_tool]
)

crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

Relaying the task output to next task as context

```

# ...

research_ai_task = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    async_execution=True,
    agent=research_agent,
    tools=[search_tool]
)

research_ops_task = Task(
    description='Find and summarize the latest AI Ops news',
    expected_output='A bullet list summary of the top 5 most important AI Ops news',
    async_execution=True,
    agent=research_agent,
    tools=[search_tool],
    async_execution=True # make this task asynchronous
)

write_blog_task = Task(
    description="Write a full blog post about the importance of AI and its latest news",
    expected_output='Full blog post that is 4 paragraphs long',
    agent=writer_agent,
    context=[research_ai_task, research_ops_task]
)

```

Example of call back function that is triggered
after task completion

```
# ...

def callback_function(output: TaskOutput):
    # Do something after the task is completed
    # Example: Send an email to the manager
    print(f"""
        Task completed!
        Task: {output.description}
        Output: {output.raw}
    """)

research_task = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[search_tool],
    callback=callback_function
)

#...

# ...
task1 = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[search_tool]
)
```

### A specific task can be accessed as show below

```

crew = Crew( agents=[research_agent],
tasks=[task1, task2, task3], verbose=True )

result = crew.kickoff()

# Returns a TaskOutput object with the description and results of the task

print(f""" Task completed! Task:
{task1.output.description} Output:
{task1.output.raw} """)

```

### Save output to a file

```
# ...

save_output_task = Task(
    description='Save the summarized AI news to a file',
    expected_output='File saved successfully',
    agent=research_agent,
    tools=[file_save_tool],
    output_file='outputs/ai_news_summary.txt',
    create_directory=True
)

#...

```

Understanding and utilizing crews in the crewAI
framework with comprehensive attributes and
functionalities.

What is a Crew? A crew in crewAI represents a
collaborative group of agents working together to
achieve a set of tasks. Each crew defines the
strategy for task execution, agent collaboration,
and the overall workflow.

```
# Example crew execution
crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[research_task, write_article_task],
    verbose=True
)

crew_output = crew.kickoff()

# Accessing the crew output
print(f"Raw Output: {crew_output.raw}")

if crew_output.json_dict:
    print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
if crew_output.pydantic:
    print(f"Pydantic Output: {crew_output.pydantic}")
print(f"Tasks Output: {crew_output.tasks_output}")
print(f"Token Usage: {crew_output.token_usage}")

```

The output of a crew in the CrewAI framework is
encapsulated within the CrewOutput class. This
class provides a structured way to access results
of the crew’s execution, including various formats
such as raw strings, JSON, and Pydantic models.
The CrewOutput includes the results from the final
task output, token usage, and individual task
outputs.

Different Ways to Kick Off a Crew Once your crew
is assembled, initiate the workflow with the
appropriate kickoff method.

CrewAI provides several methods for better control
over the kickoff process: kickoff(),
kickoff_for_each(), kickoff_async(), and
kickoff_for_each_async().

kickoff(): Starts the execution process according
to the defined process flow.

kickoff_for_each(): Executes tasks for each agent
individually.

kickoff_async(): Initiates the workflow
asynchronously.

kickoff_for_each_async(): Executes tasks for each
agent individually in an asynchronous manner.

```

### Flows in CrewAI:

Introduction

CrewAI Flows is a powerful feature designed to streamline the creation and management of AI workflows. Flows allow developers
to combine and coordinate coding tasks and
Crews efficiently, providing a robust framework
for building sophisticated AI automations.

Flows allow you to create structured, event-driven
workflows. They provide a seamless way to connect
multiple tasks, manage state, and control the flow
of execution in your AI applications. With Flows,
you can easily design and implement multi-step
processes that leverage the full potential
of CrewAI’s capabilities.

Simplified Workflow Creation: Easily chain together
multiple Crews and tasks to create complex
AI workflows.

State Management: Flows make it super easy to
manage and share state between different tasks
in your workflow.

Event-Driven Architecture: Built on an event-driven
model, allowing for dynamic and responsive
workflows.

Flexible Control Flow: Implement conditional logic,
loops, and branching within your workflows.

Input Flexibility: Flows can accept inputs to initialize
or update their state, with different handling
for structured and unstructured state management.

### Structured State Management
In structured state management, the flow’s
state is defined using a Pydantic BaseModel. Inputs must match the model’s schema, and any updates will overwrite the default values.

```

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ExampleState(BaseModel): counter: int = 0
message: str = ""

class StructuredExampleFlow(Flow[ExampleState]):
@start() def first_method(self): # Implementation

flow = StructuredExampleFlow()
flow.kickoff(inputs={"counter": 10}) ```

Unstructured State Management In unstructured
state management, the flow’s state is a
dictionary. You can pass any dictionary to update
the state.

````
from crewai.flow.flow import Flow, listen, start

class UnstructuredExampleFlow(Flow):
    @start()
    def first_method(self):
        # Implementation

flow = UnstructuredExampleFlow()
flow.kickoff(inputs={"counter": 5, "message": "Initial message"})```
````

@start() The @start() decorator is used to mark a
method as the starting point of a Flow. When a
Flow is started, all the methods decorated with
@start() are executed in parallel. You can have
multiple start methods in a Flow, and they will
all be executed when the Flow is started.

@listen() The @listen() decorator is used to mark
a method as a listener for the output of another
task in the Flow. The method decorated with
@listen() will be executed when the specified task
emits an output. The method can access the output
of the task it is listening to as an argument.

````
from crewai.flow.flow import Flow, listen, start

class OutputExampleFlow(Flow):
    @start()
    def first_method(self):
        return "Output from first_method"

    @listen(first_method)
    def second_method(self, first_output):
        return f"Second method received: {first_output}"

flow = OutputExampleFlow()
final_output = flow.kickoff()

print("---- Final Output ----")
print(final_output)```

### You can update the state of the flow

```
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ExampleState(BaseModel):
    counter: int = 0
    message: str = ""

class StateExampleFlow(Flow[ExampleState]):

    @start()
    def first_method(self):
        self.state.message = "Hello from first_method"
        self.state.counter += 1

    @listen(first_method)
    def second_method(self):
        self.state.message += " - updated by second_method"
        self.state.counter += 1
        return self.state.message

flow = StateExampleFlow()
final_output = flow.kickoff()
print(f"Final Output: {final_output}")
print("Final State:")
print(flow.state)

```

####
Flow State Management
Managing state effectively is crucial for building reliable and maintainable AI workflows. CrewAI Flows provides robust mechanisms for both unstructured and structured state management, allowing developers to choose the approach
that best fits their application’s needs.


Structured State Management
Structured state management leverages predefined schemas to ensure consistency and type safety across the workflow. By using models like Pydantic’s BaseModel, developers can define the exact shape of the state, enabling better validation and auto-completion in development environments.

Unstructured State Management
In unstructured state management,
all state is stored in the state attribute of
the Flow class. This approach offers flexibility, enabling developers to add or modify state attributes on the fly without defining a strict schema.
```
from crewai.flow.flow import Flow, listen, start

class UnstructuredExampleFlow(Flow):

    @start()
    def first_method(self):
        self.state.message = "Hello from structured flow"
        self.state.counter = 0

    @listen(first_method)
    def second_method(self):
        self.state.counter += 1
        self.state.message += " - updated"

    @listen(second_method)
    def third_method(self):
        self.state.counter += 1
        self.state.message += " - updated again"

        print(f"State after third_method: {self.state}")

flow = UnstructuredExampleFlow()
flow.kickoff()```

```
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ExampleState(BaseModel):
    counter: int = 0
    message: str = ""

class StructuredExampleFlow(Flow[ExampleState]):

    @start()
    def first_method(self):
        self.state.message = "Hello from structured flow"

    @listen(first_method)
    def second_method(self):
        self.state.counter += 1
        self.state.message += " - updated"

    @listen(second_method)
    def third_method(self):
        self.state.counter += 1
        self.state.message += " - updated again"

        print(f"State after third_method: {self.state}")

flow = StructuredExampleFlow()
flow.kickoff()
```


Choosing Between Unstructured and Structured State Management
Use Unstructured State Management when:

The workflow’s state is simple or highly dynamic.
Flexibility is prioritized over strict state definitions.
Rapid prototyping is required without the overhead of defining schemas.
Use Structured State Management when:

The workflow requires a well-defined and consistent state structure.
Type safety and validation are important for your application’s reliability.
You want to leverage IDE features like auto-completion and type checking for better developer experience.
````

Flow Control Conditional logic:

Conditional Logic: and The and\_ function in Flows
allows you to listen to multiple methods and
trigger the listener method only when all the
specified methods emit an output.

```
from crewai.flow.flow import Flow, and_, listen, start

class AndExampleFlow(Flow):

    @start()
    def start_method(self):
        self.state["greeting"] = "Hello from the start method"

    @listen(start_method)
    def second_method(self):
        self.state["joke"] = "What do computers eat? Microchips."

    @listen(and_(start_method, second_method))
    def logger(self):
        print("---- Logger ----")
        print(self.state)

flow = AndExampleFlow()
flow.kickoff()

```

Conditional Logic: or The or\_ function in Flows
allows you to listen to multiple methods and
trigger the listener method when any of the
specified methods emit an output.

```
from crewai.flow.flow import Flow, listen, or_, start

class OrExampleFlow(Flow):

    @start()
    def start_method(self):
        return "Hello from the start method"

    @listen(start_method)
    def second_method(self):
        return "Hello from the second method"

    @listen(or_(start_method, second_method))
    def logger(self, result):
        print(f"Logger: {result}")

flow = OrExampleFlow()
flow.kickoff()

```

Router The @router() decorator in Flows allows you
to define conditional routing logic based on the
output of a method. You can specify different
routes based on the output of the method, allowing
you to control the flow of execution dynamically.

```
import random
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

class ExampleState(BaseModel):
    success_flag: bool = False

class RouterFlow(Flow[ExampleState]):

    @start()
    def start_method(self):
        print("Starting the structured flow")
        random_boolean = random.choice([True, False])
        self.state.success_flag = random_boolean

    @router(start_method)
    def second_method(self):
        if self.state.success_flag:
            return "success"
        else:
            return "failed"

    @listen("success")
    def third_method(self):
        print("Third method running")

    @listen("failed")
    def fourth_method(self):
        print("Fourth method running")

flow = RouterFlow()
flow.kickoff()

```

#### Creating a flow with multiple crews

You can generate a new CrewAI project that
includes all the scaffolding needed to create a
flow with multiple crews by running the following
command:

crewai create flow name_of_flow

This command will generate a new CrewAI project
with the necessary folder structure. The generated
project includes a prebuilt crew called poem_crew
that is already working. You can use this crew as
a template by copying, pasting, and editing it to
create other crews.

#### Connecting Crews in main.py

The main.py file is where you create your flow and
connect the crews together. You can define your
flow by using the Flow class and the decorators
@start and @listen to specify the flow of
execution.

Crew simply is part of a method call with a flow
decorator

Here’s an example of how you can connect the
poem_crew in the main.py file:

```
#!/usr/bin/env python
from random import randint

from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.poem_crew.poem_crew import PoemCrew

class PoemState(BaseModel):
    sentence_count: int = 1
    poem: str = ""

class PoemFlow(Flow[PoemState]):

    @start()
    def generate_sentence_count(self):
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem(self):
        print("Generating poem")
        result = PoemCrew().crew().kickoff(inputs={"sentence_count": self.state.sentence_count})

        print("Poem generated", result.raw)
        self.state.poem = result.raw

    @listen(generate_poem)
    def save_poem(self):
        print("Saving poem")
        with open("poem.txt", "w") as f:
            f.write(self.state.poem)

def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()

if __name__ == "__main__":
    kickoff()

```

Adding Additional Crews Using the CLI Once you
have created your initial flow, you can easily add
additional crews to your project using the CLI.
This allows you to expand your flow’s capabilities
by integrating new crews without starting from
scratch.

To add a new crew to your existing flow, use the
following command:

crewai flow add-crew <crew_name>

#### What are Plots?

Plots in CrewAI are graphical representations of
your AI workflows. They display the various tasks,
their connections, and the flow of data between
them. This visualization helps in understanding
the sequence of operations, identifying
bottlenecks, and ensuring that the workflow logic
aligns with your expectations.

- https://github.com/crewAIInc/crewAI-examples/tree/main/email_auto_responder_flow

- https://github.com/crewAIInc/crewAI-examples/tree/main/lead-score-flow

- https://github.com/crewAIInc/crewAI-examples/tree/main/write_a_book_with_flows

- https://github.com/crewAIInc/crewAI-examples/tree/main/self_evaluation_loop_flow

### What is Knowledge?

The Knowledge class in CrewAI manages various
sources that store information, which can be
queried and retrieved by AI agents. This modular
approach allows you to integrate diverse data
formats such as text, PDFs, spreadsheets, and more
into your AI workflows.

Additionally, we have specific tools for generate
knowledge sources for strings, text files, PDF’s,
and Spreadsheets. You can expand on any source
type by extending the KnowledgeSource class.

```
from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Create a knowledge source
content = "Users name is John. He is 30 years old and lives in San Francisco."
string_source = StringKnowledgeSource(
    content=content, metadata={"preference": "personal"}
)

# Create an agent with the knowledge store
agent = Agent(
    role="About User",
    goal="You know everything about the user.",
    backstory="""You are a master at understanding people and their preferences.""",
    verbose=True
)

task = Task(
    description="Answer the following questions about the user: {question}",
    expected_output="An answer to the question.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge={"sources": [string_source], "metadata": {"preference": "personal"}}, # Enable knowledge by adding the sources here. You can also add more sources to the sources list.
)

result = crew.kickoff(inputs={"question": "What city does John live in and how old is he?"})

...
string_source = StringKnowledgeSource(
    content="Users name is John. He is 30 years old and lives in San Francisco.",
    metadata={"preference": "personal"}
)
crew = Crew(
    ...
    knowledge={
        "sources": [string_source],
        "metadata": {"preference": "personal"},
        "embedder_config": {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
    },
)

```

Large Language Models (LLMs) in CrewAI Large
Language Models (LLMs) are the backbone of
intelligent agents in the CrewAI framework. This
guide will help you understand, configure, and
optimize LLM usage for your CrewAI projects.

​ Key Concepts LLM: Large Language Model, the AI
powering agent intelligence Agent: A CrewAI entity
that uses an LLM to perform tasks Provider: A
service that offers LLM capabilities (e.g.,
OpenAI, Anthropic, Ollama, more providers)

Updating the agents.yaml file

```
researcher:
    role: Research Specialist
    goal: Conduct comprehensive research and analysis to gather relevant information,
        synthesize findings, and produce well-documented insights.
    backstory: A dedicated research professional with years of experience in academic
        investigation, literature review, and data analysis, known for thorough and
        methodical approaches to complex research questions.
    verbose: true
    llm: openai/gpt-4o
    # llm: azure/gpt-4o-mini
    # llm: gemini/gemini-pro
    # llm: anthropic/claude-3-5-sonnet-20240620
    # llm: bedrock/anthropic.claude-3-sonnet-20240229-v1:0
    # llm: mistral/mistral-large-latest
    # llm: ollama/llama3:70b
    # llm: groq/llama-3.2-90b-vision-preview
    # llm: watsonx/meta-llama/llama-3-1-70b-instruct
    # llm: nvidia_nim/meta/llama3-70b-instruct
    # llm: sambanova/Meta-Llama-3.1-8B-Instruct
    # ...

from crewai import LLM

llm = LLM(model="gpt-4", temperature=0.7)
agent = Agent(llm=llm, ...)

from crewai import LLM

llm = LLM(
    model="custom-model-name",
    base_url="https://api.your-provider.com/v1",
    api_key="your-api-key"
)
agent = Agent(llm=llm, ...)


```

Understanding Processes Processes orchestrate the
execution of tasks by agents, akin to project
management in human teams. These processes ensure
tasks are distributed and executed efficiently, in
alignment with a predefined strategy.

Process Implementations

Sequential: Executes tasks sequentially, ensuring
tasks are completed in an orderly progression.

Hierarchical: Organizes tasks in a managerial
hierarchy, where tasks are delegated and executed
based on a structured chain of command. A manager
language model (manager_llm) or a custom manager
agent (manager_agent) must be specified in the
crew to enable the hierarchical process,
facilitating the creation and management of tasks
by the manager.

Consensual Process (Planned): Aiming for
collaborative decision-making among agents on task
execution, this process type introduces a
democratic approach to task management within
CrewAI. It is planned for future development and
is not currently implemented in the codebase.

Process Class: Detailed Overview The Process class
is implemented as an enumeration (Enum), ensuring
type safety and restricting process values to the
defined types (sequential, hierarchical). The
consensual process is planned for future
inclusion, emphasizing our commitment to
continuous development and innovation.

Sequential Process This method mirrors dynamic
team workflows, progressing through tasks in a
thoughtful and systematic manner. Task execution
follows the predefined order in the task list,
with the output of one task serving as context for
the next.

To customize task context, utilize the context
parameter in the Task class to specify outputs
that should be used as context for subsequent
tasks.

Hierarchical Process Emulates a corporate
hierarchy, CrewAI allows specifying a custom
manager agent or automatically creates one,
requiring the specification of a manager language
model (manager_llm). This agent oversees task
execution, including planning, delegation, and
validation. Tasks are not pre-assigned; the
manager allocates tasks to agents based on their
capabilities, reviews outputs, and assesses task
completion.

```
from crewai import Crew
from crewai.process import Process
from langchain_openai import ChatOpenAI

# Example: Creating a crew with a sequential process
crew = Crew(
    agents=my_agents,
    tasks=my_tasks,
    process=Process.sequential
)

# Example: Creating a crew with a hierarchical process
# Ensure to provide a manager_llm or manager_agent
crew = Crew(
    agents=my_agents,
    tasks=my_tasks,
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4")
    # or
    # manager_agent=my_manager_agent
)

```

Collaboration Exploring the dynamics of agent
collaboration within the CrewAI framework,
focusing on the newly integrated features for
enhanced functionality.

​ Collaboration Fundamentals Collaboration in
CrewAI is fundamental, enabling agents to combine
their skills, share information, and assist each
other in task execution, embodying a truly
cooperative ecosystem.

Information Sharing: Ensures all agents are
well-informed and can contribute effectively by
sharing data and findings. Task Assistance: Allows
agents to seek help from peers with the required
expertise for specific tasks. Resource Allocation:
Optimizes task execution through the efficient
distribution and sharing of resources among
agents.

Delegation (Dividing to Conquer) Delegation
enhances functionality by allowing agents to
intelligently assign tasks or seek help, thereby
amplifying the crew’s overall capability.

​ Implementing Collaboration and Delegation
Setting up a crew involves defining the roles and
capabilities of each agent. CrewAI seamlessly
manages their interactions, ensuring efficient
collaboration and delegation, with enhanced
customization and monitoring features to adapt to
various operational needs.

​ Example Scenario Consider a crew with a
researcher agent tasked with data gathering and a
writer agent responsible for compiling reports.
The integration of advanced language model
management and process flow attributes allows for
more sophisticated interactions, such as the
writer delegating complex research tasks to the
researcher or querying specific information,
thereby facilitating a seamless workflow.

Memory

Leveraging memory systems in the CrewAI framework
to enhance agent capabilities.

Introduction to Memory Systems in CrewAI

The crewAI framework introduces a sophisticated
memory system designed to significantly enhance
the capabilities of AI agents. This system
comprises short-term memory, long-term memory,
entity memory, and contextual memory, each serving
a unique purpose in aiding agents to remember,
reason, and learn from past interactions.

How Memory Systems Empower Agents Contextual

Awareness: With short-term and contextual memory,
agents gain the ability to maintain context over a
conversation or task sequence, leading to more
coherent and relevant responses.

Experience Accumulation: Long-term memory allows
agents to accumulate experiences, learning from
past actions to improve future decision-making and
problem-solving.

Entity Understanding: By maintaining entity
memory, agents can recognize and remember key
entities, enhancing their ability to process and
interact with complex information.

Component Description

Short-Term Memory Temporarily stores recent
interactions and outcomes using RAG, enabling
agents to recall and utilize information relevant
to their current context during the current
executions.

Long-Term Memory Preserves valuable insights and
learnings from past executions, allowing agents to
build and refine their knowledge over time.

Entity Memory Captures and organizes information
about entities (people, places, concepts)
encountered during tasks, facilitating deeper
understanding and relationship mapping. Uses RAG
for storing entity information.

Contextual Memory Maintains the context of
interactions by combining ShortTermMemory,
LongTermMemory, and EntityMemory, aiding in the
coherence and relevance of agent responses over a
sequence of tasks or a conversation

User Memory Stores user-specific information and
preferences, enhancing personalization and user
experience.

Implementing Memory in Your Crew When configuring
a crew, you can enable and customize each memory
component to suit the crew’s objectives and the
nature of tasks it will perform. By default, the
memory system is disabled, and you can ensure it
is active by setting memory=True in the crew
configuration. The memory will use OpenAI
embeddings by default, but you can change it by
setting embedder to a different model. It’s also
possible to initialize the memory instance with
your own instance.

The ‘embedder’ only applies to Short-Term Memory
which uses Chroma for RAG. The Long-Term Memory
uses SQLite3 to store task results. Currently,
there is no way to override these storage
implementations. The data storage files are saved
into a platform-specific location found using the
appdirs package, and the name of the project can
be overridden using the CREWAI_STORAGE_DIR
environment variable.

```
from crewai import Crew, Agent, Task, Process

# Assemble your crew with memory capabilities
my_crew = Crew(
    agents=[...],
    tasks=[...],
    process="Process.sequential",
    memory=True,
    long_term_memory=EnhanceLongTermMemory(
        storage=LTMSQLiteStorage(
            db_path="/my_data_dir/my_crew1/long_term_memory_storage.db"
        )
    ),
    short_term_memory=EnhanceShortTermMemory(
        storage=CustomRAGStorage(
            crew_name="my_crew",
            storage_type="short_term",
            data_dir="//my_data_dir",
            model=embedder["model"],
            dimension=embedder["dimension"],
        ),
    ),
    entity_memory=EnhanceEntityMemory(
        storage=CustomRAGStorage(
            crew_name="my_crew",
            storage_type="entities",
            data_dir="//my_data_dir",
            model=embedder["model"],
            dimension=embedder["dimension"],
        ),
    ),
    verbose=True,
)

from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "openai",
        "config": {
            "model": 'text-embedding-3-small'
        }
    }
)

from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model": "mxbai-embed-large"
        }
    }
)

```

crewai reset-memories [OPTIONS]

Benefits of Using CrewAI’s Memory System 🦾
Adaptive Learning: Crews become more efficient
over time, adapting to new information and
refining their approach to tasks. 🫡 Enhanced
Personalization: Memory enables agents to remember
user preferences and historical interactions,
leading to personalized experiences. 🧠 Improved
Problem Solving: Access to a rich memory store
aids agents in making more informed decisions,
drawing on past learnings and contextual insights.

Planning Learn how to add planning to your CrewAI
Crew and improve their performance.

​ Introduction The planning feature in CrewAI
allows you to add planning capability to your
crew. When enabled, before each Crew iteration,
all Crew information is sent to an AgentPlanner
that will plan the tasks step by step, and this
plan will be added to each task description.

​ Using the Planning Feature Getting started with
the planning feature is very easy, the only step
required is to add planning=True to your Crew:

Planning LLM Now you can define the LLM that will
be used to plan the tasks. You can use any
ChatOpenAI LLM model available.

When running the base case example, you will see
something like the output below, which represents
the output of the AgentPlanner responsible for
creating the step-by-step logic to add to the
Agents’ tasks.

```
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI

# Assemble your crew with planning capabilities and custom LLM
my_crew = Crew(
    agents=self.agents,
    tasks=self.tasks,
    process=Process.sequential,
    planning=True,
    planning_llm=ChatOpenAI(model="gpt-4o")
)

# Run the crew
my_crew.kickoff()

```
