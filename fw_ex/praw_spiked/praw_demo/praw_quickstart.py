import praw
import os
from dotenv import load_dotenv

load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ["CLIENTID"],
    client_secret=os.environ["CLIENTSEC"],
    password=os.environ["PASSWORD"],
    user_agent="keep-alive",
    username=os.environ["REDNAME"],
)

print(reddit.read_only)

# assume you have a praw.Reddit instance bound to variable `reddit`
subreddit = reddit.subreddit("redditdev")

print(subreddit.display_name)
# Output: redditdev
print(subreddit.title)
# Output: reddit development
print(subreddit.description)

# assume you have a Subreddit instance bound to variable `subreddit`
for submission in subreddit.hot(limit=10):
    print(submission.title)
    # Output: the submission's title
    print(submission.score)
    # Output: the submission's score
    print(submission.id)
    # Output: the submission's ID
    print(submission.url)
    # Output: the URL the submission points to or the submission's URL if it's a self post
    
# assume you have a Submission instance bound to variable `submission`
redditor1 = submission.author
print(redditor1.name)
# Output: name of the redditor

# assume you have a praw.Reddit instance bound to variable `reddit`
redditor2 = reddit.redditor("bboe")
print(redditor2.link_karma)
# Output: u/bboe's karma
