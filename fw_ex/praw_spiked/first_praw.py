# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "praw",
#     "python-dotenv",
# ]
# ///
import praw

import os
from dotenv import load_dotenv

load_dotenv()

reddit_instance = praw.Reddit(
    client_id=os.environ["CLIENTID"],
    client_secret=os.environ["CLIENTSEC"],
    user_agent="keep-alive",
    username=os.environ["REDNAME"],
    password=os.environ["PASSWORD"],
)

print(reddit_instance)
print(reddit_instance.user.me())


# get some popular subreddits
def pop_subreddit():
    for subreddit in reddit_instance.subreddits.popular(limit=10):
        print(subreddit.display_name)


test_grounds = reddit_instance.subreddit("testingground4bots")

print(test_grounds.display_name)

# print("Post to Testing Grounds")
# test_grounds.submit(
#     "this is a test from uv env", selftext="Lets get this moving people"
# )

# print("Posts in Testing Grounds")
# for post in test_grounds.top(limit=10):
#     print(post.title)

print("New Posts in Testing Grounds")
for post in test_grounds.new(limit=1):
    print(post.title)
    print(post.id)

# interacting with the submission
my_subid = "1ja7hj2"
submission = reddit_instance.submission(id=my_subid)
print(submission.title)

submission.reply("Where are your uv env")

# print("Comments in Testing Grounds")
# for comment in test_grounds.comments(limit=10):
#     print(comment.__dict__)

print("Get submission comments")
for comment in submission.comments:
    print(comment.body)

print("Replying to the comment")
for comment in submission.comments:
    comment.reply("Let me reply to you")

url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
suburl = reddit_instance.submission(url=url)
print(suburl.title)

suburl.comments.replace_more(limit=0)
for top_level_comment in suburl.comments:
    print(top_level_comment.body)
