import praw
import datetime
import re
import csv

reddit = praw.Reddit()


# write code for making this list based on  my own csv file
stockList = {"TSLA": {"TSLA", "Tesla"}, "SPY": {"SPY"}, 
             "RDDT": {"RDDT", "Reddit"}, "ALCC": {"ALCC"}, "OKLO": {"OKLO"}}

mentions = dict.fromkeys(stockList.keys(), 0)

def getMentions(subredditName, numberOfPosts):
    subreddit = reddit.subreddit(subredditName)
    
    hotPosts = subreddit.hot(limit=numberOfPosts)

    # go through every post
    for post in hotPosts:
        # Avoids memes
        if post.link_flair_text == "Meme":
            continue
        
        # Cycles through our list of stock symbols
        for stockName in stockList.keys():
            # Cyclces through variations of stock symbols
            for variation in stockList[stockName]:
                if re.search(r'\$?' + variation + r'\$?', post.title) or re.search(r'\$?' + variation + r'\$?', post.selftext):
                    mentions[stockName] += 1

                #maybe search in comments as well?

# Obtaining Mentions
getMentions("wallstreetbets", 100)
getMentions("stockmarket", 100)
getMentions("investing", 20)
getMentions("wallstreetbets", 20)
getMentions("stocks", 20)
getMentions("options", 20)
getMentions("robinhood", 20)
getMentions("securityanalysis", 20)
getMentions("daytrading", 20)

print("\n\n-RESULTS-")

for stockName in mentions:
    if mentions[stockName] != 0:
        print(f"{stockName}: {mentions[stockName]}")