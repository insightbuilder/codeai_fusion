from pywebio.input import input, input_group, FLOAT
from pywebio.output import put_text


def get_box_dimensions():
    dimensions = input_group(
        "Enter Box Dimensions",
        [
            input("Length:", name="length", type=FLOAT, placeholder="Enter length"),
            input("Width:", name="width", type=FLOAT, placeholder="Enter width"),
            input("Height:", name="height", type=FLOAT, placeholder="Enter height"),
        ],
    )

    put_text(
        f"Box Dimensions: Length = {dimensions['length']}, Width = {dimensions['width']}, Height = {dimensions['height']}"
    )


get_box_dimensions()


# from pywebio.input import input
# from pywebio.output import put_text, put_markdown
# from pydantic import BaseModel, Field

# pyright: reportMissingImports=false


# class Box(BaseModel):
#     length: int = Field(description="Length of the box", default=None)
#     width: int = Field(description="Width of the box", default=None)
#     depth: int = Field(description="Depth of the box", default=None)
#    unit: str = Field(description="Unit of measurement of the box", default=None)


# put_markdown("## Welcome to Pydantic Agent with Form")

# data_points = ["length", "width", "depth", "unit"]

# while True:
#     put_text("Provide the Length, Width, Depth and Unit of the box")
#     box = Box()
#     for data_point in data_points:
#         your_prompt = input(f"{data_point}: ")
#         if your_prompt == "" or your_prompt == "bye":
#             break
#         put_text(f"You: {your_prompt}")
#         setattr(box, data_point, your_prompt)

#     put_text(f"Final Box: {box}")
