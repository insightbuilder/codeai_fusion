from composio import ComposioToolSet, App
import os

# toolset = ComposioToolSet(entity_id="testrun", api_key=os.getenv("COMPOSIO_API_KEY"))
toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

entity = toolset.get_entity()
# request = entity.initiate_connection(App.GOOGLECALENDAR)
# request = entity.initiate_connection(App.GMAIL)
request = entity.initiate_connection(App.GITHUB)

print(f"Open this URL to authenticate: {request.redirectUrl}")
