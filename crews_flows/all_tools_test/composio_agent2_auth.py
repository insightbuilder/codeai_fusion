from composio import ComposioToolSet, App
import os

# This file is for authenticating agent2
# related applications. Application like
# Gmail, Github etc

toolset = ComposioToolSet(entity_id="agent2", api_key=os.getenv("COMPOSIO_API_KEY"))

entity = toolset.get_entity()
request = entity.initiate_connection(App.GMAIL)

print(f"Open this URL to authenticate agent2: {request.redirectUrl}")
