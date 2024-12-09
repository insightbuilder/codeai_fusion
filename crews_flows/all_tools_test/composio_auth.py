from composio import ComposioToolSet, App

toolset = ComposioToolSet(entity_id="testrun")
entity = toolset.get_entity()
# request = entity.initiate_connection(App.GOOGLECALENDAR)
request = entity.initiate_connection(App.GMAIL)

print(f"Open this URL to authenticate: {request.redirectUrl}")
