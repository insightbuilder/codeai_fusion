from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Echo")


@mcp.tool()
def bmi_calculator(weight: float, height: float) -> str:
    """Calculates the BMI using the given weight and height, and returns the value"""
    if height > 0 and weight > 0:
        bmi = round(weight / (height**2), 2)

        return f"Your BMI: {bmi}"

    return "Height and weight have to be more than 0"


@mcp.tool()
def custom_eqn(a: float, b: float, d: float) -> float:
    """Performs a custom equation with the given parameters and returns the result"""
    x = 25
    c = a + b * b
    return a * (x ^ 3) - b * (x ^ 2) + c * x - d


if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
