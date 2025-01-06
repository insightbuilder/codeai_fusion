from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, UserError
from pywebio.input import input
from pywebio.output import put_text
import traceback
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false


class Box(BaseModel):
    x: int = Field(description="Length of the box", default=None)
    y: int = Field(description="Width of the box", default=None)
    z: int = Field(description="Depth of the box", default=None)
    unit: str = Field(description="Unit of measurement of the box", default=None)


# Having a type / class that is opposite to what you want
class NoBox(BaseModel):
    "When box dimensions are not extracted"


measure_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt=(
        "Extract the dimension of the box from given input"
        # "You should use the tools available with you"
        "You must extract all part of the Box dimension"
    ),
    result_type=Box | NoBox,
    retries=2,
)


@measure_agent.tool
async def extract_dimensions(
    ctx: RunContext, length: int, width: int, depth: int, unit: str
) -> Box:
    """Used for extracting the dimensions of the box"""
    put_text("Inside Tool")
    return Box(x=length, y=width, z=depth, unit=unit)


@measure_agent.result_validator
async def validate(ctx: RunContext, result: Box | NoBox) -> Box | NoBox:
    """Validate whether the result is Box or Not"""
    put_text("Entering Validator")
    put_text("Result inside Validator:", result)
    if isinstance(result, NoBox) or not result:
        raise UserError("Box Not found. Give the box dimensions")
    else:
        return result


while True:
    your_prompt = input("You: ")
    if your_prompt == "" or your_prompt == "bye":
        break
    put_text(f"You: {your_prompt}")
    try:
        result = measure_agent.run_sync(your_prompt)
        missing_dims = []
        if result.data.x is None:
            missing_dims.append("Length Missing")
        if result.data.y is None:
            missing_dims.append("Width Missing")
        if result.data.z is None:
            missing_dims.append("Depth Missing")
        if result.data.unit is None:
            missing_dims.append("Unit Missing")
        if len(missing_dims) > 0:
            put_text(f"Missing Dimensions: {', '.join(missing_dims)}")
        else:
            put_text("Given Dimensions are: ", result.data)
            confirm = input("Please confirm the above (y/n): ")
            if confirm == "y":
                put_text("Dimensions confirmed")
            else:
                put_text("Give length, width, breadth and units of the box")
                continue

        put_text(
            f"Pydantic Agent: Confirmed dimensions are  {result.data}"
        )  # print(result.data)

    except Exception as e:
        print(e)
        put_text(traceback.format_exc())
