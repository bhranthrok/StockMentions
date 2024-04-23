import praw
import pandas
import datetime

reddit = praw.Reddit()

# importing subreddits we care about
wallStreetBets = reddit.subreddit("wallstreetbets")

top_posts = wallStreetBets.top(limit=3)

print(top_posts)