# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "flask",
#     "praw",
#     "python-dotenv",
# ]
# ///
from flask import Flask, render_template, request
import praw
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()


app = Flask(__name__)


reddit = praw.Reddit(
    client_id=os.environ["CLIENTID"],
    client_secret=os.environ["CLIENTSEC"],
    user_agent="keep-alive",
    username=os.environ["REDNAME"],
    password=os.environ["PASSWORD"],
)


# 🔹 Home Route
@app.route("/")
def home():
    return render_template("index.html")


# 🔹 1. Find Subreddits
@app.route("/search_subreddits", methods=["POST"])
def search_subreddits():
    keyword = request.form.get("keyword")
    results = reddit.subreddits.search(keyword, limit=10)
    subreddits = [
        {
            "name": sub.display_name,
            "subscribers": sub.subscribers,
            "url": f"https://www.reddit.com/r/{sub.display_name}/",
        }
        for sub in results
    ]

    return render_template("index.html", subreddits=subreddits, keyword=keyword)


# 🔹 2. Get Trending Posts
@app.route("/trending_posts", methods=["POST"])
def trending_posts():
    subreddit_name = request.form.get("subreddit")
    sort_by = request.form.get("sort_by", "hot")

    subreddit = reddit.subreddit(subreddit_name)
    posts = getattr(subreddit, sort_by)(limit=5)

    trending = [
        {
            "title": post.title,
            "comments": post.num_comments,
            "score": post.score,
            "url": post.url,
        }
        for post in posts
    ]

    return render_template(
        "index.html", trending=trending, subreddit_name=subreddit_name
    )


# 🔹 3. Search Posts Globally
@app.route("/search_posts", methods=["POST"])
def search_posts():
    query = request.form.get("query")
    results = reddit.subreddit("all").search(query, sort="relevance", limit=10)

    posts = [
        {
            "subreddit": str(post.subreddit),
            "title": post.title,
            "comments": post.num_comments,
            "score": post.score,
            "url": post.url,
        }
        for post in results
    ]

    return render_template("index.html", posts=posts, query=query)


# 🔹 4. Filter High Engagement Posts
@app.route("/high_engagement_posts", methods=["POST"])
def high_engagement_posts():
    query = request.form.get("query")
    min_upvotes = int(request.form.get("min_upvotes", 10))
    min_comments = int(request.form.get("min_comments", 0))
    days = int(request.form.get("days", 7))  # Default to last 7 days

    # Use datetime.now(timezone.utc) to get the current UTC time
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)

    results = reddit.subreddit("all").search(
        query, sort="relevance", limit=50
    )  # Fetch latest posts
    filtered_posts = []
    for post in results:
        # Convert created_utc timestamp to a timezone-aware datetime object
        post_date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)

        if (
            post.score >= min_upvotes
            and post.num_comments >= min_comments
            and post_date >= cutoff_time
        ):
            filtered_posts.append({
                "subreddit": str(post.subreddit),
                "title": post.title,
                "comments": post.num_comments,
                "score": post.score,
                "url": post.url,
                "date": post_date.strftime("%Y-%m-%d %H:%M:%S UTC"),  # Format date
            })

    return render_template(
        "index.html", filtered_posts=filtered_posts, query=query, days=days
    )


if __name__ == "__main__":
    app.run(debug=True)
