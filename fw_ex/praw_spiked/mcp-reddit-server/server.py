from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
import praw
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()

# Creating a Reddit authorized instance

reddit = praw.Reddit(
    client_id=os.environ["AID"],
    client_secret=os.environ["ASEC"],
    user_agent="keep-alive",
    username=os.environ["ANAME"],
    password=os.environ["APASS"],
)

# Creating a MCP Server
mcp = FastMCP("vabired")


@mcp.tool()
def get_trending_posts(subreddit: str) -> str:
    """Returns the treding hot posts in given subreddit.
    The topic, post body and upvotes are returned in text format"""
    trending_posts = ""
    # getting 5 posts that are in hot list
    subreddit = reddit.subreddit(subreddit)
    posts = getattr(subreddit, "hot")(limit=10)

    for post in posts:
        # arranging them in the trending post variable
        trending_posts += f"Topic: {post.title}\n"
        trending_posts += f"score: {post.score}\n"
        trending_posts += f"url: {post.url}\n"

    return trending_posts


if __name__ == "__main__":
    print("Server Starts")
    mcp.run()
