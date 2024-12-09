from composio import Composio, App

client = Composio()
entity = client.get_entity(id="testrun")

# Enable trigger with optional config parameter
entity.enable_trigger(app=App.GMAIL, trigger_name="gmail_new_gmail_message", config={})
# Disable trigger by ID (if needed)
# entity.disable_trigger("gmail_new_gmail_message")
