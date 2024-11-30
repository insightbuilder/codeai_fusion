---
id: 1732795671-KCBU
aliases:
  - Tools of the CrewAI
tags: []
---

# Tools of the CrewAI

Introduction CrewAI tools empower agents with
capabilities ranging from web searching and data
analysis to collaboration and delegating tasks
among coworkers. This documentation outlines how
to create, integrate, and leverage these tools
within the CrewAI framework, including a new focus
on collaboration tools.

What is a Tool? A tool in CrewAI is a skill or
function that agents can utilize to perform
various actions. This includes tools from the
CrewAI Toolkit and LangChain Tools, enabling
everything from simple searches to complex
interactions and effective teamwork among agents.

Key Characteristics of Tools Utility: Crafted for
tasks such as web searching, data analysis,
content generation, and agent collaboration.
Integration: Boosts agent capabilities by
seamlessly integrating tools into their workflow.
Customizability: Provides the flexibility to
develop custom tools or utilize existing ones,
catering to the specific needs of agents. Error
Handling: Incorporates robust error handling
mechanisms to ensure smooth operation. Caching
Mechanism: Features intelligent caching to
optimize performance and reduce redundant
operations.

Available CrewAI Tools Error Handling: All tools
are built with error handling capabilities,
allowing agents to gracefully manage exceptions
and continue their tasks.

Caching Mechanism: All tools support caching,
enabling agents to efficiently reuse previously
obtained results, reducing the load on external
resources and speeding up the execution time. You
can also define finer control over the caching
mechanism using the cache_function attribute on
the tool.

Tool Description

BrowserbaseLoadTool A tool for interacting with
and extracting data from web browsers.
CodeDocsSearchTool A RAG tool optimized for
searching through code documentation and related
technical documents.

CodeInterpreterTool A tool for interpreting python
code.

ComposioTool Enables use of Composio tools.

CSVSearchTool A RAG tool designed for searching
within CSV files, tailored to handle structured
data.

DALL-E Tool A tool for generating images using the
DALL-E API.

DirectorySearchTool A RAG tool for searching
within directories, useful for navigating through
file systems.

DOCXSearchTool A RAG tool aimed at searching
within DOCX documents, ideal for processing Word
files.

DirectoryReadTool Facilitates reading and
processing of directory structures and their
contents.

EXASearchTool A tool designed for performing
exhaustive searches across various data sources.

FileReadTool Enables reading and extracting data
from files, supporting various file formats.

FirecrawlSearchTool A tool to search webpages
using Firecrawl and return the results.

FirecrawlCrawlWebsiteTool A tool for crawling
webpages using Firecrawl.

FirecrawlScrapeWebsiteTool A tool for scraping
webpages URL using Firecrawl and returning its
contents.

GithubSearchTool A RAG tool for searching within
GitHub repositories, useful for code and
documentation search.

SerperDevTool A specialized tool for development
purposes, with specific functionalities under
development.

TXTSearchTool A RAG tool focused on searching
within text (.txt) files, suitable for
unstructured data.

JSONSearchTool A RAG tool designed for searching
within JSON files, catering to structured data
handling.

LlamaIndexTool Enables the use of LlamaIndex
tools.

MDXSearchTool A RAG tool tailored for searching
within Markdown (MDX) files, useful for
documentation.

PDFSearchTool A RAG tool aimed at searching within
PDF documents, ideal for processing scanned
documents.

PGSearchTool A RAG tool optimized for searching
within PostgreSQL databases, suitable for database
queries.

Vision Tool A tool for generating images using the
DALL-E API.

RagTool A general-purpose RAG tool capable of
handling various data sources and types.

ScrapeElementFromWebsiteTool Enables scraping
specific elements from websites, useful for
targeted data extraction.

ScrapeWebsiteTool Facilitates scraping entire
websites, ideal for comprehensive data collection.

WebsiteSearchTool A RAG tool for searching website
content, optimized for web data extraction.

XMLSearchTool A RAG tool designed for searching
within XML files, suitable for structured data
formats.

YoutubeChannelSearchTool A RAG tool for searching
within YouTube channels, useful for video content
analysis.

YoutubeVideoSearchTool A RAG tool aimed at
searching within YouTube videos, ideal for video
data extraction

```

from crewai.tools import BaseTool


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = "Clear description for what this tool is useful for, your agent will need this information to use it."

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "Result from custom tool"

from crewai.tools import tool

@tool
def multiplication_tool(first_number: int, second_number: int) -> str:
    """Useful for when you need to multiply two numbers together."""
    return first_number * second_number

def cache_func(args, result):
    # In this case, we only cache the result if it's a multiple of 2
    cache = result % 2 == 0
    return cache

multiplication_tool.cache_function = cache_func

writer1 = Agent(
        role="Writer",
        goal="You write lessons of math for kids.",
        backstory="You're an expert in writing and you love to teach kids but you know nothing of math.",
        tools=[multiplication_tool],
        allow_delegation=False,
    )
    #...

```

Conclusion Tools are pivotal in extending the
capabilities of CrewAI agents, enabling them to
undertake a broad spectrum of tasks and
collaborate effectively.

When building solutions with CrewAI, leverage both
custom and existing tools to empower your agents
and enhance the AI ecosystem. Consider utilizing
error handling, caching mechanisms, and the
flexibility of tool arguments to optimize your
agents’ performance and capabilities.

Create Custom Tools Comprehensive guide on
crafting, using, and managing custom tools within
the CrewAI framework, including new
functionalities and error handling.

​ Creating and Utilizing Tools in CrewAI This
guide provides detailed instructions on creating
custom tools for the CrewAI framework and how to
efficiently manage and utilize these tools,
incorporating the latest functionalities such as
tool delegation, error handling, and dynamic tool
calling. It also highlights the importance of
collaboration tools, enabling agents to perform a
wide range of actions.

​ Subclassing BaseTool To create a personalized
tool, inherit from BaseTool and define the
necessary attributes, including the args_schema
for input validation, and the \_run method.

```
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = "What this tool does. It's vital for effective utilization."
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, argument: str) -> str:
        # Your tool's logic here
        return "Tool's result"

```

Using the tool Decorator Alternatively, you can
use the tool decorator @tool. This approach allows
you to define the tool’s attributes and
functionality directly within a function, offering
a concise and efficient way to create specialized
tools tailored to your needs.

```
from crewai.tools import tool

@tool("Tool Name")
def my_simple_tool(question: str) -> str:
    """Tool description for clarity."""
    # Tool logic here
    return "Tool output"

```

Defining a Cache Function for the Tool To optimize
tool performance with caching, define custom
caching strategies using the cache_function
attribute.

```
@tool("Tool with Caching")
def cached_tool(argument: str) -> str:
    """Tool functionality description."""
    return "Cacheable result"

def my_cache_strategy(arguments: dict, result: str) -> bool:
    # Define custom caching logic
    return True if some_condition else False

cached_tool.cache_function = my_cache_strategy

```
