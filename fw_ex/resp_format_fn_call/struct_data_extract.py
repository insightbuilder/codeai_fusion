from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()


class MediumArticleExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]


completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure.",
        },
        {
            "role": "user",
            "content": """
        🎁 Happy Outcome Bias Wednesday, y’all!
Issue #151: getting real about how science works, and the value of doing nothing
By Scott Lamb

It’s Hump Day for Cognitive Bias Week, and time to address one of the thornier issues of being a human and having a brain like ours: What to do when there’s not enough meaning.

This feels like an existential issue for us, as it’s just hard-wired into our perception of reality: There’s so much information in the world, but we’re only able to perceive a tiny fraction of it, and we need to operate from there to make decisions and do things. This creates holes in our mental models, and our brains hate holes, and will do anything they can to fill them.

One particular way we do this is forgetting that our current thinking doesn’t perfectly map to the past or future. This is especially tricky around decision-making — I’d like to introduce you now to our little friend, outcome bias: When we judge the quality of our decision based on the outcome, rather than the quality of the decision-making (based on the available information we had at the time we made it). A quick example: A start-up founder who has a crazy idea for a product; regardless of the quality of her thinking, she’s a genius if it’s a success and a failure if it bombs.

Why should you worry about outcome bias? Cassie Kozyrkov, the former Chief Decision Scientist at Google, has written about this extensively over the years on Medium, and sees it as an especially costly kind of cognitive bias, and a threat to our ability to “promote and retain competent leaders.” It leads to more conservative decision-making when people are most afraid of the thing they can’t control, the outcome.

So what can you do? Here are three tips for mitigating outcome bias in your decisions:

Try to make fewer decisions — this can mean building more structure or delegating more often.
Focus on how you decide, not just what — keep a decision journal to help you track your process
Only make good decisions — this doesn’t mean just ones with good outcomes!
⚡ Lightning round: great, recent Medium stories in one sentence or less
Professor of philosophy Soazig Le Bihan wants to help us all set up better expectations around what science is (and isn’t) — it’s best understood as a complex, collaborative, and occasionally fallible practice of trying to understand our complicated world, rather than something that can or should provide pure, precise, and definitive answers in all cases.
Adam DeMartino, the former founder and COO of mushroom company Smallhold, gives a pretty thorough accounting of what happened to his company after they failed to make hard decisions early, took on venture capital, and eventually went into bankruptcy — all in all, a fascinating look at how one of the big business successes coming out of Covid failed spectacularly.
Your daily dose of practical wisdom: on doing nothing
The next time you’ve got a free ten minutes in your schedule, what if instead of quickly checking email or browsing the latest headlines, you simply… did nothing? There’s a lot of value to be had in just being alone with your thoughts — it’s good for creativity, and lowering stress — so try to cultivate a mini-habit of doing nothing.
        """,
        },
    ],
    response_format=MediumArticleExtraction,
)

research_paper = completion.choices[0].message.parsed

print(research_paper)
