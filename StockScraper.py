import praw
import datetime
import re
import csv

reddit = praw.Reddit()

stockList = {}

# regex pattern test
'''
stringList = []
stringList.append("Apple buys stock")
stringList.append("$Apple buys stock")
stringList.append("Apple$ buys stock")
stringList.append("Stocks Apple buys")
stringList.append("Stocks pineapple buys")
pattern = r'(?:^|\s|\$)' + re.escape("Apple") + r'(?=\s|$|\'s)?'

for string in stringList:
     match = re.search(pattern, string)
     print(f"string: {string}, result: {match}")
     
'''

# Creates dictionary of stock tickers and their multiple variations.
with open(r"F:\Projects\StockMentions\StockMentions\NASDAQ Name Extraction\StockVariations.csv", 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        stockTicker = row[0] # Eg. "AAPL"

        if stockTicker == "Ticker(Key)": #ignores the labels row
            continue
        
        stockList[stockTicker] = [] # start the list
        currentColumn = 1
        while True:
            try: 
                currentVariation = row[currentColumn] # Eg. "Apple"
                stockList[stockTicker].append(currentVariation)

                if row[currentColumn + 1] == '':
                    break                
                
                currentColumn += 1
            except IndexError:
                break

mentions = dict.fromkeys(stockList.keys(), 0) # Tracks results

def getMentions(subredditName, numberOfPosts):
    subreddit = reddit.subreddit(subredditName)
    
    hotPosts = subreddit.hot(limit=numberOfPosts)

    # go through every post
    for post in hotPosts:
        # Avoids memes
        if post.link_flair_text == "Meme":
            continue

        title = post.title
        body = post.selftext

        print(title)

        # Cycles through our list of stock symbols
        for stockName in stockList.keys():
            # Cycles through variations of stock symbols
            if len(stockName) == 1:
                continue
            for variation in stockList[stockName]:

                regexPattern = r'(?:^|\s|\$)' + re.escape(variation) + r'(?=\s|$|\'s)?'
                # OLD REGEX PATTERNS
                # r'(?:\s|\b|\$)' + re.escape(variation) + r'(?:\s|\b|\$|\'s)?'
                # r'(?:\b|\$)' + re.escape(variation) + r'(?:\b|\$)'
                # r'\s+\$?' + variation + r'\$?\s+'

                '''
                matchesTitle = re.findall(regexPattern, title)
                matchesBody = re.findall(regexPattern, body)
                mentions[stockName] += len(matchesTitle) + len(matchesBody)
                '''
                
                if re.search(regexPattern, title) or re.search(regexPattern, body):
                    mentions[stockName] += 1
                    print(f"found {stockName}")
                
                #maybe search in comments as well?


# Obtaining Mentions
getMentions("wallstreetbets", 20)
getMentions("stockmarket", 20)
getMentions("investing", 20)
getMentions("stocks", 20)
getMentions("options", 20)
getMentions("robinhood", 20)
getMentions("securityanalysis", 20)
getMentions("daytrading", 20)

# sort results
# Could write this onto a file very easily
print("\n\n-RESULTS-")

for stockName in mentions:
    # Avoids inevitable margin of error
    if mentions[stockName] > 3:
        print(f"{stockName}: {mentions[stockName]}")