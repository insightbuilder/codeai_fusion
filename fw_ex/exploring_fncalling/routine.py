import openai
from dotenv import load_dotenv

# Note the below inspect module, which is
# part of the Python. This helps to review the
# objects/ classes, functions inside python
import inspect
import json


# This is part of the routine.py module,
# which is in the same location as the auto_handoff.py
# function that creates the schemas
def function_to_schema(func) -> dict:
    # the type_map dictionary for different python objekts
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }
    # we are going to extract the signature of the func function
    # that is sent as the parameter to this function
    try:
        # extracts the names, arguments
        signature = inspect.signature(func)
        # if the parameter is wrongly sent, then below error
        # vwill be raised
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )
    # next we need to extract the parameters of the func function,
    # and store before returning it,
    parameters = {}
    # building the parameter schema
    # from the extracted "Signature" we extract the parameters
    for param in signature.parameters.values():
        try:
            # here we use the type_map dict to find the annotation of the parameter type
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            # if the parameter is of Unknown type then we have to raise the error
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}
    # then we need to assign if any of the parameter is required compulsorily
    # for the func function to be called...
    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]
    # below is the schema, that is being built with the aboev collected data
    return {
        "type": "function",  # this is type
        "function": {
            "name": func.__name__,  # name is directly extracted
            "description": (func.__doc__ or "").strip(),  # docstrings for description
            "parameters": {  # Parameters for the function
                "type": "object",
                "properties": parameters,  # this is list of parameters
                "required": required,  # this is the required_list of parameter
            },
        },
    }


# Let take the 1st function as example
def look_up_item(search_query):
    # fn_name is look_up_item
    # type is Function
    # parameter is search_query, of type string
    # this parameter is required.
    # All the above info is extracted from the function_to_schema function
    """Use to find item ID.
    Search query can be a description or keywords."""

    # return hard-coded item ID - in reality would be a lookup
    return "item_132612938"


# 2nd function
def execute_refund(item_id, reason="not provided"):
    print("Summary:", item_id, reason)  # lazy summary
    return "success"


def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"Assistant: {name}({args})")

    # call corresponding function with provided arguments
    return tools_map[name](**args)


def run_full_turn(system_message, tools, messages):
    num_init_messages = len(messages)
    messages = messages.copy()

    while True:
        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in tools]
        tools_map = {tool.__name__: tool for tool in tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_message}] + messages,
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


if __name__ == "__main__":
    load_dotenv(".env")
    client = openai.OpenAI()
    messages = []
    model = "gpt-4o-mini"

    tools = [execute_refund, look_up_item]

    # Customer Service Routine
    system_message = (
        "You are a customer support agent for ACME Inc."
        "Always answer in a sentence or less."
        "Follow the following routine with the user:"
        "1. First, ask probing questions and understand the user's problem deeper.\n"
        " - unless the user has already provided a reason.\n"
        "2. Propose a fix (make one up).\n"
        "3. ONLY if not satesfied, offer a refund.\n"
        "4. If accepted, search for the ID and then execute refund."
        ""
    )

    while True:
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})

        new_messages = run_full_turn(system_message, tools, messages)
        messages.extend(new_messages)
        # user: Look up black currant
        # model: Returns the Id after using look_up_item python function
        # user: I need a refund
        # model: returns refund success after running execute_refund python function
        # Two activity done by one agent...
