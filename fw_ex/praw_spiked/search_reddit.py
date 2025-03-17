# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "praw",
#     "python-dotenv",
# ]
# ///

import praw
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id=os.environ["CLIENTID"],
    client_secret=os.environ["CLIENTSEC"],
    username=os.environ["REDNAME"],
    password=os.environ["PASSWORD"],
    user_agent="keep-alive",
)

# Search across all subreddits
query = "Cursor"
results = reddit.subreddit("all").search(query, limit=10)  # Search globally

# Print results
for post in results:
    print(f"Subreddit: r/{post.subreddit}")
    print(f"Title: {post.title}")
    print(f"URL: {post.url}")
    print(f"Upvotes: {post.score}")
    print("-" * 40)
