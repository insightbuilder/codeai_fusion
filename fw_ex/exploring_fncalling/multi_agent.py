from openai import OpenAI
from dotenv import load_dotenv
import json
from pydantic import BaseModel
from routine import function_to_schema, execute_tool_call, execute_refund, look_up_item


class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o-mini"
    instructions: str = "You are super helpful agent"
    tools: list = []


# the full_turn is run using agent as parameter
def run_full_turn(agent, messages):
    num_init_messages = len(messages)
    messages = messages.copy()

    while True:
        # turn python functions into tools and save a reverse map
        # observe the agent.tools are used for building
        tool_schemas = [function_to_schema(tool) for tool in agent.tools]
        tools_map = {tool.__name__: tool for tool in agent.tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model=agent.model,
            messages=[{"role": "system", "content": agent.instructions}] + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:  # print assistant response
            print("Assistant:", message.content)

        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools_map)

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    # ==== 3. return new messages =====
    return messages[num_init_messages:]


def place_order(item_name):
    "Places the order"
    return f"Order for {item_name} placed"


if __name__ == "__main__":
    load_dotenv(".env")
    client = OpenAI()
    refund_agent = Agent(
        name="Refunder",
        instructions="You are refund agent, handle refund requests",
        tools=[execute_refund],
    )

    sales_agent = Agent(
        name="Sales Executive", instructions="Sell user a product", tools=[place_order]
    )
    messages = []
    # observe that user query is manually hard coded
    # and then agents are also hard coded
    user_query = "Place order for Black currant"
    print(f"User query: {user_query}")
    messages.append({"role": "user", "content": user_query})

    # get response for agents to run
    response = run_full_turn(sales_agent, messages)
    messages.extend(response)

    # user changes mind, asks for refund
    user_query = "I made a mistake, provide me a refund"
    print(f"User query: {user_query}")
    response = run_full_turn(refund_agent, messages)
    messages.extend(response)
