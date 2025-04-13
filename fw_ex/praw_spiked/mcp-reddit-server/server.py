from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
import praw
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from anthropic import Anthropic

load_dotenv()
anthropic = Anthropic()

# Creating a sync Reddit authorized instance

reddit = praw.Reddit(
    client_id=os.environ["AID"],
    client_secret=os.environ["ASEC"],
    user_agent="keep-alive",
    username=os.environ["ANAME"],
    password=os.environ["APASS"],
)


# Creating a MCP Server
mcp = FastMCP("mcp-vabired")


@mcp.tool()
def get_trending_posts(subreddit: str) -> str:
    """Returns the treding hot posts in given subreddit.
    The topic, post body and upvotes are returned in text format"""
    trending_posts = ""
    # getting 10 posts that are in hot list
    subreddit = reddit.subreddit(subreddit)
    posts = getattr(subreddit, "hot")(limit=10)

    for post in posts:
        # arranging them in the trending post variable
        trending_posts += f"Topic: {post.title}\n"
        trending_posts += f"score: {post.score}\n"
        trending_posts += f"url: {post.url}\n"
    # returns the post title, score and url in text form
    return trending_posts


@mcp.prompt()
def get_reply(comment: str) -> str:
    """Prompt to get a suitable reply for a comment"""
    return f"Review this {comment} and provide a suitable polite response"


@mcp.prompt()
def reply_with_context(context: str, query: str) -> str:
    """Prompt to get the LLM to use the context and answer a query"""
    return f"Review this {context} and answer the {query} precisely"


@mcp.resource("subreddit://info")
def subreddit_info_static() -> str:
    """Returns the details of SideProject & Webdev subreddit"""

    with open("subred_data.txt", "r") as f:
        name_desc_details = f.read()
    return name_desc_details


# @mcp.tool()
# async def get_subreddit_info(query: str, ctx: Context) -> str:
#     """Answer the user query by accessing the subreddit_info from
#     get_subreddit resource. Use the reply_with_context prompt"""

#     info = await ctx.read_resource("subreddit_info")
#     # making the prompt
#     prompt = mcp.get_prompt(
#         "reply_with_context", arguments={"context": info, "query": query}
#     )
#     # Building messages
#     messages = [
#         {
#             "role": "user",
#             "content": prompt,
#         }
#     ]
#     # Calling the model
#     response = anthropic.messages.create(
#         model="claude-3-5-haiku-20241022",
#         max_tokens=500,
#         messages=messages,
#     )
#     # returning the reply.
#     return response.content[0].text


@mcp.tool()
def reply_comment(comment_text: str) -> str:
    """Returns a suitable polite reply for the comment"""
    # Building the prompt using get_reply
    prompt = mcp.get_prompt("get_reply", arguments={"comment": comment_text})
    messages = [
        {
            "role": "user",
            "content": prompt,
        },
    ]
    # calling the model with the prompt
    response = anthropic.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=500,
        messages=messages,
    )

    return response.content[0].text


if __name__ == "__main__":
    mcp.run()
