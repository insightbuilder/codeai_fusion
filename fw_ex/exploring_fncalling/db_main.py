# flake8: noqa: E501

import datetime
import random
from openai import OpenAI

# from swarm.agents import create_triage_agent
import database

# from swarm import Agent
from dotenv import load_dotenv
from auto_handoff import run_repl, Agent


# 1st transfer agent function, observe it takes no params
# and Returns an Agent...
def transfer_to_sales_agent():
    """User for anything sales or buying related."""
    return sales_agent  # This is how the conversation is handed over to the next agent


# THis is for transfering to starting agent...called problem triage agent
def transfer_back_to_triage():
    """Call this if the user brings up a topic outside of your purview,
    including escalating to human."""
    return triage_agent


# THis is for transfering to refunds agent...called problem triage agent
def transfer_to_refund():
    """Call this if the user requires refund"""
    return refunds_agent


def show_pdt_price():
    """Provides the available products and the price of each product and its pdt_id"""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM PRODUCTS""")
    result = cursor.fetchall()
    data = ""
    for row in result:
        data += str(row)
    return data


def refund_item(user_id, item_id):
    """Initiate a refund based on the user ID and item ID.
    Takes as input arguments in the format '{"user_id":"1","item_id":"3"}'
    """
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT amount FROM PurchaseHistory
        WHERE user_id = ? AND item_id = ?
    """,
        (user_id, item_id),
    )
    result = cursor.fetchone()
    if result:
        amount = result[0]
        return f"Refunding ${amount} to user ID {user_id} for item ID {item_id}."
    else:
        return f"No purchase found for user ID {user_id} and item ID {item_id}."


def notify_customer(user_id, method):
    """Notify a customer by their preferred method of either phone or email.
    Takes as input arguments in the format '{"user_id":"1","method":"email"}"""

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT email, phone FROM Users
        WHERE user_id = ?
    """,
        (user_id,),
    )
    user = cursor.fetchone()
    if user:
        email, phone = user
        if method == "email" and email:
            return f"Emailed customer {email} a notification."
        elif method == "phone" and phone:
            return f"Texted customer {phone} a notification."
        else:
            return f"No {method} contact available for user ID {user_id}."
    else:
        return f"User ID {user_id} not found."


def order_item(user_id, product_id):
    """Place an order for a product based on the user ID and product ID.
    Takes as input arguments in the format '{"user_id":"1","product_id":"2"}'"""
    date_of_purchase = datetime.datetime.now()
    item_id = random.randint(1, 300)

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT product_id, product_name, price FROM Products
        WHERE product_id = ?
    """,
        (product_id,),
    )
    result = cursor.fetchone()
    if result:
        product_id, product_name, price = result
        print(
            f"Ordering product {product_name} for user ID {user_id}. The price is {price}."
        )
        # Add the purchase to the database
        database.add_purchase(user_id, date_of_purchase, item_id, price)
        return f"""Added product for user_id:{user_id},
        with dop: {date_of_purchase}, for item_id: {item_id} at price: {price}"""
    else:
        return f"Product {product_id} not found."


# Initialize the database
database.initialize_database()

# Preview tables
database.preview_table("Users")
database.preview_table("PurchaseHistory")
database.preview_table("Products")

# Define the agents

refunds_agent = Agent(
    name="Refunds Agent",
    model="gpt-4o-mini",
    description="""You are a refund agent that handles all actions related to refunds after a return has been processed.
    You must ask for both the user ID and item ID to initiate a refund. Ask for both user_id and item_id in one message.
    If the user asks you to notify them, you must ask them what their preferred method of notification is. For notifications, you must
    ask them for user_id and method in one message.""",
    tools=[refund_item, notify_customer, transfer_back_to_triage],
)

sales_agent = Agent(
    name="Sales Agent",
    model="gpt-4o-mini",
    description="""You are a sales agent that handles all actions related to placing an order to purchase an item.
    Regardless of what the user wants to purchase, must ask for BOTH the user ID and product ID to place an order.
    An order cannot be placed without these two pieces of inforamation. Ask for both user_id and product_id in one message.
    If the user asks you to notify them, you must ask them what their preferred method is. For notifications, you must
    ask them for user_id and method in one message. If user asks to show the product list, then you can show it using 
    show_pdt_price
    """,
    tools=[order_item, notify_customer, transfer_back_to_triage, show_pdt_price],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are to triage a users request, and call a tool to transfer to the right intent.
    Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
    You dont need to know specifics, just the topic of the request.
    If the user request is about making an order or purchasing an item, transfer to the Sales Agent.
    If the user request is about getting a refund on an item or returning a product, transfer to the Refunds Agent.
    When you need more information to triage the request to an agent, ask a direct question without explaining why you're asking it.
    Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of user.""",
    tools=[transfer_to_refund, transfer_to_sales_agent],
)

for f in triage_agent.tools:
    print(f.__name__)

if __name__ == "__main__":
    load_dotenv(".env")
    client = OpenAI()
    # Run the demo loop
    run_repl(entry_agent=triage_agent, client=client)
