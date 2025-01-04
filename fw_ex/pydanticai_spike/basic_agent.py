from pydantic_ai import Agent

agent = Agent("openai:gpt-4o-mini", system_prompt="Reply in a single sentence")

result = agent.run_sync("Where is center of universe")

print(result.data)
