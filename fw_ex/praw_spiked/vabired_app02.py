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
    client_id=os.environ["AID"],
    client_secret=os.environ["ASEC"],
    user_agent="keep-alive",
    username=os.environ["ANAME"],
    password=os.environ["APASS"],
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search_subreddits", methods=["GET", "POST"])
def search_subreddits():
    subreddits = []
    keyword = ""

    if request.method == "POST":
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

    return render_template(
        "search_subreddits.html", subreddits=subreddits, keyword=keyword
    )


@app.route("/trending_posts", methods=["GET", "POST"])
def trending_posts():
    trending = []
    subreddit_name = "ProgrammingHumor"

    if request.method == "POST":
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
        "trending_posts.html", trending=trending, subreddit_name=subreddit_name
    )


@app.route("/search_posts", methods=["GET", "POST"])
def search_posts():
    posts = []
    query = ""

    if request.method == "POST":
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

    return render_template("search_posts.html", posts=posts, query=query)


@app.route("/high_engagement_posts", methods=["GET", "POST"])
def high_engagement_posts():
    filtered_posts = []
    query = ""
    min_upvotes = 3
    min_comments = 0
    days = 30

    if request.method == "POST":
        query = request.form.get("query")
        min_upvotes = int(request.form.get("min_upvotes", 3))
        min_comments = int(request.form.get("min_comments", 0))
        days = int(request.form.get("days", 30))
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)

        results = reddit.subreddit("all").search(query, sort="relevance", limit=50)
        for post in results:
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
                    "date": post_date.strftime("%Y-%m-%d %H:%M:%S UTC"),
                })

    return render_template(
        "high_engagement_posts.html",
        filtered_posts=filtered_posts,
        query=query,
        days=days,
    )


if __name__ == "__main__":
    app.run(debug=True)
