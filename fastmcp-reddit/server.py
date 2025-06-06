# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp",
#     "praw",
#     "python-dotenv",
#     "anthropic",
# ]
# ///
from mcp.server.fastmcp import FastMCP
import praw
from dotenv import load_dotenv
import os
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


@mcp.prompt()
def get_reply(comment: str) -> str:
    """Prompt to get a suitable reply for a comment"""
    return f"Review this {comment} and provide a suitable polite response"


@mcp.prompt()
def reply_with_context(context: str, query: str) -> str:
    """Prompt to get the LLM to use the context and answer a query"""
    return f"Review this {context} and answer the {query} precisely"


# dynamic template resource
@mcp.resource("reddit://search/{query}")
def search_reddit(query: str) -> str:
    """Searches the entire reddit and returns the post title, content, and score along with URL"""
    results = reddit.subreddit("all").search(query, sort="relevance", limit=10)
    posts = ""
    for post in results:
        posts += f"subreddit: {str(post.subreddit)} \n title: {post.title} \n comments: {post.num_comments} \n score: {post.score} \n url: {post.url}"
    return posts


# Static Resource
@mcp.resource("subreddit://info")
def subreddit_info_static() -> str:
    """Returns the details of SideProject & Webdev subreddit by reading a local file"""
    with open("subred_data.txt", "r") as f:
        name_desc_details = f.read()
    return name_desc_details


# Tool that uses a dynamic resource with templates
@mcp.tool()
async def search_for_me(query: str) -> str:
    """Searches the entire reddit and returns the post title, content, and score along with URL"""
    resource_query = f"reddit://search/{query}"
    reddit_data = await mcp.read_resource(resource_query)
    return reddit_data[0].content


# Tool that calls an API
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


# Tool that uses a static resource
@mcp.tool()
# async def get_subreddit_info(query: str) -> Iterable[ReadResourceContents]:
async def get_subreddit_info(query: str) -> str:
    """Used for answering the user query relating to subreddit informations"""

    data = await mcp.read_resource("subreddit://info")
    # making the prompt
    prompt = await mcp.get_prompt(
        "reply_with_context",
        arguments={"context": data[0].content, "query": query},
    )
    # returning the reply.
    # return prompt.model_dump_json()
    return prompt.messages[0].content.text


# Tool that uses LLM inside the server to get a reply.
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
    print("Starting MCP Server")
    mcp.run()
