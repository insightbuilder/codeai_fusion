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


reddit = praw.Reddit(
    client_id=os.environ["CLIENTID"],
    client_secret=os.environ["CLIENTSEC"],
    user_agent="keep-alive",
    username=os.environ["REDNAME"],
    password=os.environ["PASSWORD"],
)


# 🔹 1. Find relevant subreddits for a topic
def find_subreddits(keyword, limit=10):
    print(f"\n🔎 Searching for subreddits related to '{keyword}'...\n")
    results = reddit.subreddits.search(keyword, limit=limit)

    for sub in results:
        print(f"r/{sub.display_name} - {sub.subscribers} subscribers")
        print(f"🔗 URL: https://www.reddit.com/r/{sub.display_name}/\n")


# 🔹 2. Get trending posts from a subreddit
def get_trending_posts(subreddit_name, sort_by="hot", limit=5):
    print(f"\n🔥 Trending posts in r/{subreddit_name} ({sort_by})...\n")
    subreddit = reddit.subreddit(subreddit_name)

    if sort_by == "hot":
        posts = subreddit.hot(limit=limit)
    elif sort_by == "new":
        posts = subreddit.new(limit=limit)
    elif sort_by == "top":
        posts = subreddit.top(limit=limit)
    else:
        posts = subreddit.hot(limit=limit)

    for post in posts:
        print(f"📌 {post.title}")
        print(f"💬 {post.num_comments} comments | 👍 {post.score} upvotes")
        print(f"🔗 URL: {post.url}\n")


# 🔹 3. Search posts globally
def search_posts(query, limit=10, sort_by="relevance"):
    print(f"\n🔎 Searching for '{query}' across all subreddits...\n")
    results = reddit.subreddit("all").search(query, sort=sort_by, limit=limit)

    for post in results:
        print(f"🏷️ [{post.subreddit}] {post.title}")
        print(f"💬 {post.num_comments} comments | 👍 {post.score} upvotes")
        print(f"🔗 URL: {post.url}\n")


# 🔹 4. Filter posts by engagement
def filter_high_engagement_posts(query, min_upvotes=100, min_comments=10, limit=20):
    print(f"\n📈 Searching for highly engaging posts about '{query}'...\n")
    results = reddit.subreddit("all").search(query, limit=limit)

    for post in results:
        if post.score >= min_upvotes and post.num_comments >= min_comments:
            print(f"🏷️ [{post.subreddit}] {post.title}")
            print(f"💬 {post.num_comments} comments | 👍 {post.score} upvotes")
            print(f"🔗 URL: {post.url}\n")


# 🔹 Run sample searches
find_subreddits("machine learning", limit=5)
get_trending_posts("learnpython", sort_by="hot", limit=3)
search_posts("Python web scraping", limit=5, sort_by="top")
filter_high_engagement_posts("AI startup", min_upvotes=500, min_comments=50, limit=10)
