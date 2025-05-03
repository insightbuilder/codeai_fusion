from scrapegraphai.graphs import SmartScraperGraph
import os
import json

# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": os.environ["OPENAI_API_KEY"],
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": False,
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract useful information from the webpage, including a description of what the company does, founders and social media links",
    source="https://scrapegraphai.com/",
    config=graph_config,
)

# Run the pipeline
result = smart_scraper_graph.run()


print(json.dumps(result, indent=4))
