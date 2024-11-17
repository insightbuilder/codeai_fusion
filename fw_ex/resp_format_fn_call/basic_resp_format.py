#!/bin/python3

from pydantic import BaseModel
from openai import OpenAI, LengthFinishReasonError

client = OpenAI()


class Step(BaseModel):
    explanation: str
    output: str


class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str


completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
        },
        {"role": "user", "content": "how can I solve 8x + 7 = -23"},
    ],
    response_format=MathReasoning,
)

math_reasoning = completion.choices[0].message.parsed

print(math_reasoning)

try:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
            },
            {"role": "user", "content": "how can I solve 8x + 7 = -23"},
        ],
        response_format=MathReasoning,
        max_tokens=50,
    )
    math_response = completion.choices[0].message
    if math_response.parsed:
        print(math_response.parsed)
    elif math_response.refusal:
        # handle refusal
        print(math_response.refusal)
except Exception as e:
    # Handle edge cases
    if type(e) is LengthFinishReasonError:
        # Retry with a higher max tokens
        print("Too many tokens: ", e)
        pass
    else:
        # Handle other exceptions
        print(e)
        pass
