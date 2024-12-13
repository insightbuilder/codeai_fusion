from composio import ComposioToolSet, App
import os

# This file is for authenticating agent1
# related applications. Application like
# Gmail, Github etc

toolset = ComposioToolSet(entity_id="agent1", api_key=os.getenv("COMPOSIO_API_KEY"))

entity = toolset.get_entity()
request = entity.initiate_connection(App.GMAIL)

print(f"Open this URL to authenticate agent1: {request.redirectUrl}")
