from composio_openai import ComposioToolSet, Action
from openai import OpenAI
from composio import Trigger

openai_client = OpenAI()
composio_toolset = ComposioToolSet()


listener = composio_toolset.create_trigger_listener()


# Triggers when a new event takes place
@listener.callback(filters={"trigger_name": Trigger.GMAIL_NEW_GMAIL_MESSAGE})
def callback_function(event):
    # Parse event data and perform actions
    payload = event.payload
    thread_id = payload.get("threadId")
    message = payload.get("messageText")
    sender_mail = payload.get("sender")
    print(sender_mail + ":" + message)


listener.wait_forever()
