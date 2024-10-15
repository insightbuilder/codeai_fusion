# Imports for LLM
from openai import OpenAI
from dotenv import load_dotenv

# Json is required for parsing the function args
import json

# Pydantic is use for structing the Agents & Response
from pydantic import BaseModel
from typing import Optional

# Converting the python function to dictionary of schema
from routine import function_to_schema
# We will look at the function_to_schema first
# We have seen the walkthrough, lets proceed


# In case of Auto Handoff, there are Agents, with models, instruction, and tools


class Agent(BaseModel):
    # we can see the agent class inherits the Pydantic's BaseModel class
    name: str = "Agent"  # name
    model: str = "gpt-4o-mini"  # Different agents can have Different models
    instructions: str = "You are a helpful agent"  # base line instruction
    tools: list = []  # This is the key, tools that the agents have


class Response(BaseModel):
    # This is a object, that encapsulates the Agents
    # when being returned
    agent: Optional[Agent]
    # This response carries with it the messages list...
    # this is how the chat memorry is available for different
    # agents
    messages: list


# This is th important function where the logic of Agents,
# function returns from function calling comes together...
# We need to look at the supporting functions & Transfer functions...
# Lets do that...
# Lets not look at run_full_turn function, here you will understand
# how agents work...
def run_full_turn(agent, messages, client):
    # here the agent persona is assigned
    current_agent = agent
    # the history of messages is recievd as list
    num_init_messages = len(messages)
    # they are cloned for local use
    messages = messages.copy()
    # loop until the agents come to resolution
    while True:
        # turn python functions into tools and save a reverse map
        # the function_to_schema function that we saws helps in creating the
        # list of tools and attaches them to the tool_schemas list
        tool_schemas = [function_to_schema(tool) for tool in current_agent.tools]
        tools = {tool.__name__: tool for tool in current_agent.tools}
        # then the tools and their names are mapped into tools dictionary,
        # this is the dictionary used in execute_tool_call function...

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            # the current agent contains the model
            model=agent.model,
            # the messages are going to be taken from the agents entering
            # instructions are extracted
            messages=[{"role": "system", "content": current_agent.instructions}]
            + messages,  # messages are appended
            tools=tool_schemas or None,  # tools are sent along
        )
        message = response.choices[0].message
        messages.append(message)
        # this is where the current_agent name is displayed before the loop starts
        if message.content:  # print agent response
            print(f"{current_agent.name}:", message.content)
        # if LLM doesn't have tool_calls, then script stops
        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===
        # depending on the tool_calls, various functions gets called
        for tool_call in message.tool_calls:
            # transferring or executing, both are function calls
            result = execute_tool_call(tool_call, tools, current_agent.name)
            # here is the key, the return of the functions can be
            # agents to which we want to hand over next
            # THis is the place where next agent handover happens
            if type(result) is Agent:  # if agent transfer, update current agent
                # here the agent is being changed
                current_agent = result
                result = (
                    f"Transfered to {current_agent.name}. Adopt persona immediately."
                )
            # in regular function case, there is no issue,
            # it just returns the functions' return string
            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            # that infor is appended to the messages list
            messages.append(result_message)

    # ==== 3. return last agent used and new messages =====
    # see how the Response object contains the current_agent, which is already
    # updated if there was a agent transfer, else it will maintain the old agent
    # primary difference is whether the function called returns string / does some
    # operation or returns agent...
    return Response(agent=current_agent, messages=messages[num_init_messages:])
    # thats is the end... Yep


# 1st supporting function, which executes the function_calling with the arguments
# observe, it takes tool_call, tools dictionary map and the agent_name,
# we will see, how these are built in some time...
def execute_tool_call(tool_call, tools, agent_name):
    # name is extracted
    name = tool_call.function.name
    # function arguments are parsed into args dictionary
    args = json.loads(tool_call.function.arguments)
    # This is where the agent_name is shown... After the function is called
    print(f"{agent_name}:", f"{name}({args})")
    # Finally the call is executed
    return tools[name](**args)  # call corresponding function with provided arguments


# This is were agent specific tools comes to life,
# Observe the docstring, the name of the function,
# and its return value... In the below case the function
# is used for escalating to human, and exit the loop


def escalate_to_human(summary):
    """Only call this if explicitly asked to."""
    # The docstring helps the LLM to decide when to use the function
    print("Escalating to human agent...")
    print("\n=== Escalation Report ===")
    print(f"Summary: {summary}")
    print("=========================\n")
    exit()  # this built in function will exit the while loop of the script


# 1st transfer agent function, observe it takes no params
# and Returns an Agent...
def transfer_to_sales_agent():
    """User for anything sales or buying related."""
    return sales_agent  # This is how the conversation is handed over to the next agent


# this is for transfering to issues_and_repairs_agent
def transfer_to_issues_and_repairs():
    """User for issues, repairs, or refunds."""
    return issues_and_repairs_agent


# THis is for transfering to starting agent...called problem triage agent
def transfer_back_to_triage():
    """Call this if the user brings up a topic outside of your purview,
    including escalating to human."""
    return triage_agent


# Here we will see the agents being built
# First the Triage agent, observe the name, instructions
# and the tools
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer service bot for ACME Inc. "
        "Introduce yourself. Always be very brief. "
        "Gather information to direct the customer to the right department. "
        "But make your questions subtle and natural."
    ),
    # every agent has explicit access to agents or python function [tools], that are built above
    # This agent has access to all transfering agent functions
    tools=[transfer_to_sales_agent, transfer_to_issues_and_repairs, escalate_to_human],
)


# Following are set of support of function
# that do actual work. The agents use them as tools.
# Observe the docstring, you can figure out wht they do
def execute_order(product, price: int):
    """Price should be in USD."""
    print("\n\n=== Order Summary ===")
    print(f"Product: {product}")
    print(f"Price: ${price}")
    print("=================\n")
    # the function_calling can include input requests too
    confirm = input("Confirm order? y/n: ").strip().lower()
    if confirm == "y":
        print("Order execution successful!")
        return "Success"
    # can have their own logic... Not required to implement in prompts
    else:
        print("Order cancelled!")
        return "User cancelled order."


# Here is the Sales Agents... The instruction will sure give you a laugh...
sales_agent = Agent(
    name="Sales Agent",
    instructions=(
        "You are a sales agent for ACME Inc."
        "Always answer in a sentence or less."
        "Follow the following routine with the user:"
        "1. Ask them about any problems in their life related to catching roadrunners.\n"
        "2. Casually mention one of ACME's crazy made-up products can help.\n"
        " - Don't mention price.\n"
        "3. Once the user is bought in, drop a ridiculous price.\n"
        "4. Only after everything, and if the user says yes, "
        "tell them a crazy caveat and execute their order.\n"
        ""
    ),
    # this agent also has couple of tools
    tools=[execute_order, transfer_back_to_triage],
)


# looks up the item...
def look_up_item(search_query):
    """Use to find item ID.
    Search query can be a description or keywords."""
    item_id = "item_132612938"
    print("Found item:", item_id)
    return item_id


# executes the refund
def execute_refund(item_id, reason="not provided"):
    print("\n\n=== Refund Summary ===")
    print(f"Item ID: {item_id}")
    print(f"Reason: {reason}")
    print("=================\n")
    print("Refund execution successful!")
    return "success"


# Another agent for repairs
issues_and_repairs_agent = Agent(
    name="Issues and Repairs Agent",
    instructions=(
        # instructions are more elaborate
        "You are a customer support agent for ACME Inc."
        "Always answer in a sentence or less."
        "Follow the following routine with the user:"
        "1. First, ask probing questions and understand the user's problem deeper.\n"
        " - unless the user has already provided a reason.\n"
        "2. Propose a fix (make one up).\n"
        "3. ONLY if not satesfied, offer a refund.\n"
        "4. If accepted, search for the ID and then execute refund."
        ""
    ),
    tools=[execute_refund, look_up_item, transfer_back_to_triage],
)


# The agents and supportng functions are explained..
# before going to main, lets move to run_full_turn function above
# We have seen all the supporting functions, agents definition... lets now
# look at the main loop
# this is the loop that created the chat in the demo


## This is the run_repl that we were seeing inside db_main.py
def run_repl(entry_agent: Agent, client: OpenAI):
    # it starts with an agent, in our case it is triage
    agent = entry_agent  # The first interfacing agent
    messages = []
    # This loop keeps the user interaction with the LLM in a loop
    while True:
        user = input("User: ")
        # user query goes into the messages
        messages.append({"role": "user", "content": user})
        # start the conversation with triage agent
        # this calles the run_full_turn function, where the user request
        # used classify which function to call, with help of the LLMS
        # the function is called, and the necessary activity is completed
        # and then it returns back here...
        response = run_full_turn(agent=agent, messages=messages, client=client)
        agent = response.agent
        messages.extend(response.messages)


if __name__ == "__main__":
    load_dotenv(".env")
    # we are using the OpenAI client
    client = OpenAI()
    agent = triage_agent  # calling the triage_agent as first agent
    messages = []

    while True:
        user = input("User: ")
        # user query goes into the messages
        messages.append({"role": "user", "content": user})
        # start the conversation with triage agent
        # this calles the run_full_turn function, where the user request
        # used classify which function to call, with help of the LLMS
        # the function is called, and the necessary activity is completed
        # and then it returns back here...
        response = run_full_turn(agent=agent, messages=messages, client=client)
        agent = response.agent
        messages.extend(response.messages)
    # The loop continues, until the escalate_to_human is called
    # or ctrl+D is pressed...
