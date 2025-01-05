from pydantic_ai import Agent, RunContext
from typing import Optional
from pywebio.input import input
from pywebio.output import put_text, put_markdown
from rich import print
import traceback

roulette_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt=(
        "Be brief and terse"
        "Reply with customer's name if available"
        "Use roulette wheel tool to see"
        "If the customer has won the lottery"
        "Based on the number they provide"
        "If no name is given then check if"
        "interested and get the name to register"
    ),
)


@roulette_agent.system_prompt
async def get_customer_name(
    ctx: RunContext[dict], cust_name: Optional[str] = None
) -> str:
    """Returns the customer name from name_registry"""
    print("Check if name available\n")
    if not cust_name and len(name_registry) == 0:
        return "No name registered"

    return f"The customer's name is {cust_name}"


@roulette_agent.tool
async def register_name(ctx: RunContext[dict], your_name: str) -> str:
    """Checks if customer name is registered, else registers him."""
    print("Check if name registered")
    if your_name in ctx.deps["registry"].values():
        return f"Hi. {your_name} is registered to play"
    else:
        print("Registering Customer\n")
        idx = len(name_registry) + 1
        name_idx = f"name_{idx}"
        ctx.deps["registry"][name_idx] = your_name
        return f"Hi. {your_name} is {idx} and is registered to play"


@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[dict], square: Optional[int] = None) -> str:
    """Check if square is winner"""
    if not square:
        return "Pick a square"
    return "win" if square == ctx.deps["success"] else "lost"


# See what is in the agent parameter
# print(roulette_agent.__dict__)
# print("System Prompt: \n")
# print(roulette_agent.system_prompt.__dict__)

# Start user interaction

put_markdown("## Welcome Roulette Wheel")

name_registry = {}
success = 18
while True:
    your_prompt = input("You: ")
    if your_prompt == "" or your_prompt == "bye":
        break
    put_text(f"You: {your_prompt}")
    try:
        result = roulette_agent.run_sync(
            your_prompt, deps={"success": success, "registry": name_registry}
        )
        put_text(f"Roulette Wheel:  {result.data}")
    except Exception as e:
        put_text(f"Error: {e}")
        put_text(traceback.format_exc())
