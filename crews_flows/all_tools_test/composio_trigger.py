from composio import ComposioToolSet, App
import os
from rich import print

client = ComposioToolSet(entity_id="agent1", api_key=os.getenv("COMPOSIO_API_KEY"))
entity = client.get_entity()
print(entity.id)
# Enable trigger with optional config parameter
trigger_schema = client.get_trigger("gmail_new_gmail_message")

# print(trigger_schema.json())
enable_response = entity.enable_trigger(
    app=App.GMAIL,
    trigger_name="gmail_new_gmail_message",
    config={"userId": "me", "interval": 1, "labelIds": "INBOX"},
)
print(enable_response)

# {'status': 'success', 'triggerId': 'd30a9aeb-b181-49b7-9215-a6bfe1b422d8', 'isNew': True}

# Disable trigger by ID (if needed)
# entity.disable_trigger("d30a9aeb-b181-49b7-9215-a6bfe1b422d8")
