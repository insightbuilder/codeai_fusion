# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "praw",
#     "python-dotenv",
# ]
# ///
import praw
import time
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize PRAW with Reddit API credentials
n_reddit = praw.Reddit(
    client_id=os.environ["CLIENTID"],
    client_secret=os.environ["CLIENTSEC"],
    username=os.environ["REDNAME"],
    password=os.environ["PASSWORD"],
    user_agent="keep-alive",
)
a_reddit = praw.Reddit(
    client_id=os.environ["AID"],
    client_secret=os.environ["ASEC"],
    username=os.environ["ANAME"],
    password=os.environ["APASS"],
    user_agent="keep-alive",
)


def post_to_subreddits(subreddits, title, body=None, url=None, delay=10):
    """
    Posts a title + body (or title + URL) to multiple subreddits.

    Parameters:
        subreddits (list): List of subreddit names (e.g., ["learnpython", "technology"])
        title (str): Post title
        body (str): Post body (optional)
        url (str): URL for link post (optional)
        delay (int): Delay in seconds between posts (to avoid spam detection)
    """
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            print(f"📝 Posting to r/{subreddit_name}...")

            print("Choose a Flair in subreddit: \n")

            flair_list = list(subreddit.flair.link_templates)
            if len(flair_list) == 0:
                print("No flairs found, setting flair to None")
                flair = None
            else:
                print("****************************")
                print("Flair name \t Flair ID")
                for flair in flair_list:
                    print(f"{flair['text'][:10]}: \t {flair['id']}")
                print("****************************")
                flair = input("Enter Flair from above list: ")
            # Determine if it's a text post or a link post
            if url:
                post = subreddit.submit(title, url=url, flair_id=flair)
                print(f"✅ Posted link to r/{subreddit_name}: {post.url}")
            else:
                post = subreddit.submit(title, selftext=body, flair_id=flair)
                print(f"✅ Posted text to r/{subreddit_name}: {post.url}")

            # Avoid triggering Reddit's spam filter
            time.sleep(delay)

        except Exception as e:
            print(f"❌ Failed to post in r/{subreddit_name}: {e}")


if __name__ == "__main__":
    print("Which Account you want to use?")
    acc = int(input("1. NoEfficiency\n2. Acrobatic-Aeerie\n"))
    if acc == 2:
        reddit = a_reddit
        print(reddit.user.me(), "is Chosen")
    elif acc == 1:
        reddit = n_reddit
        print(reddit.user.me(), "is Chosen")
    else:
        print("Choose 1 or 2")
    print("Which Subreddits you want to post in?")

    subreddits_list = []

    while True:
        subreddit_name = input("Enter subreddit name (or 'done' to finish): ")
        if subreddit_name.lower() == "done":
            break
        subreddits_list.append(subreddit_name)
    print(subreddits_list)
    post_title = input("Provide Post title: ")
    post_body = input("Provide Post body: ")
    post_to_subreddits(subreddits_list, post_title, body=post_body)
