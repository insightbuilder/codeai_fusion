# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "praw",
#     "python-dotenv",
#     "pyyaml",
# ]
# ///
import praw
import time
import yaml
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
            try:
                flair_list = list(subreddit.flair.link_templates)
                print("****************************")
                print("Flair name \t Flair ID")
                for flair in flair_list:
                    print(f"{flair['text'][:10]}: \t {flair['id']}")
                print("****************************")
                flair = input("Enter Flair from above list: ")
            except Exception as e:
                print(f"Exception: {e}")
                print("No flairs found, setting flair to None")
                flair = None
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

    yaml_file = input("Enter the path to the YAML file: ")

    with open(yaml_file, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        subreddits_list = yaml_data["subreddits"]
        post_title = yaml_data["title"]
        post_body = yaml_data["body"]
        print(
            "Subreddits:",
            subreddits_list,
            "\nPost Title:",
            post_title,
            "\nPost Body:",
            post_body,
        )
        post_to_subreddits(subreddits_list, post_title, body=post_body)
