from composio_openai import ComposioToolSet, App
from openai import OpenAI
from crewai import Agent, Task, Crew, LLM
from composio_crewai import ComposioToolSet as CrewComposioToolSet

# from anthropic import Anthropic
from composio import Trigger
import os

# pyright: reportCallIssue=false

# Trigger listener made ready on llmagent21
toolset = ComposioToolSet(entity_id="agent21", api_key=os.getenv("COMPOSIO_API_KEY"))
openai_client = OpenAI()
# antropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools = toolset.get_tools(apps=[App.GMAIL])
print(len(tools))


def agent_function(thread_id: str, message: str, sender_mail: str):
    tools = toolset.get_tools(apps=[App.GMAIL])
    # here there are many tools, one of them will
    # make the message important.
    print("Entering Agent call")
    try:

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            tools=tools,
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant that can parse the email content,
                    send email reply for the recieved mail using the tools available to you.
                    You are given the thread id, message and sender of the recieved mail.""",
                },
                {
                    "role": "user",
                    "content": f"Thread ID: {thread_id}\nMessage: {message}\nSender: {sender_mail}",
                },
            ],
        )
        result = toolset.handle_tool_calls(response)
        print(result)

    except Exception as e:
        print("Error:", e)


def mail_summary_writer(thread_id: str, message: str, sender_mail: str):

    print("Entering mail_summary_writer")
    llm = LLM(
        model="anthropic/claude-3-haiku-20240307",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    crewtoolset = CrewComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

    file_tools = crewtoolset.get_tools(actions=["FILETOOL_CREATE_FILE"])

    try:
        data_write_agent = Agent(
            role="You are a mail storing writer",
            goal="""use the tools given to you and Write the bulleted summary of
            email {message} from {sender}to the textfile. use the file name in user_query""",
            backstory="You are very good in formatting and writing mails to the file",
            tools=file_tools,
            llm=llm,
            verbose=True,
        )

        data_write_task = Task(
            description="Write the recieved {message} to the given file in the {user_query} using the tools",
            expected_output="Status of file write completion",
            agent=data_write_agent,
        )

        mail_writer_crew = Crew(
            name="mail_write_crew",
            agents=[data_write_agent],
            tasks=[data_write_task],
            verbose=True,
        )
        print("reached kickoff")
        writer_output = mail_writer_crew.kickoff(
            {
                "message": message,
                "user_query": f"write the file to ./{thread_id}.txt",
                "sender": sender_mail,
            }
        )

        print(writer_output)

    except Exception as e:
        print(f"Error writing mail summary: {str(e)}")


listener = toolset.create_trigger_listener()


@listener.callback(filters={"trigger_name": Trigger.GMAIL_NEW_GMAIL_MESSAGE})
def callback_function(event):
    payload = event.payload
    thread_id = payload.get("threadId")
    message = payload.get("messageText")
    sender_mail = payload.get("sender")
    print(f"Sender Mail recieved at llmagent21: {sender_mail}")
    agent_function(thread_id, message, sender_mail)
    # mail_summary_writer(thread_id, message, sender_mail)


print("Starting listener")
listener.wait_forever()
