import praw
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import csv

app = Flask(__name__)
CORS(app)

reddit = praw.Reddit()

stockList = {}

# regex pattern test
'''
stringList = []
stringList.append("Apple buys stock")
stringList.append("$Apple buys stock")
stringList.append("Apple$ buys stock")
stringList.append("Stocks Apple buys")
stringList.append("Stocks pineApple buys")
stringList.append("Stocks AppleTree buys")
pattern = r'(?:^|\s|\$)' + "Apple" + r'(?=\$|\'s|:|\s|$)'

for string in stringList:
     match = re.search(pattern, string)
     print(f"string: {string}, result: {match}")
'''
     

# Creates dictionary of stock tickers and their multiple variations.
with open(r"F:\Projects\StockMentions\StockMentions\NASDAQ Name Extraction\StockVariations.csv", 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        stockTicker = row[0] # Eg. "AAPL"

        if stockTicker == "Ticker(Key)": # ignores the labels row
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

combinedPatterns = {}
for stockName, variations in stockList.items():
    if len(stockName) <= 2:
        continue
    combined = r'(?:^|\s|\$)' + '|'.join(re.escape(variation) for variation in variations) + r'(?=\$|\'s|:|\s|$)'
    combinedPatterns[stockName] = re.compile(combined) # pre-compile for big performance boost

mentions = dict.fromkeys(stockList.keys(), 0) # Tracks results

def getMentions(subredditName, numberOfPosts, sortingMethod):
    subreddit = reddit.subreddit(subredditName)
    
    if sortingMethod.lower() == "hot":
        posts = subreddit.hot(limit=numberOfPosts)
    elif sortingMethod.lower() == "new":
        posts = subreddit.new(limit=numberOfPosts)
    elif sortingMethod.lower() == "top":
        posts = subreddit.top(limit=numberOfPosts) 
    elif sortingMethod.lower() == "rising":
        posts = subreddit.rising(limit=numberOfPosts)


    # go through every post
    for post in posts:
        if post.link_flair_text == "Meme":
            continue

        title = post.title
        body = post.selftext

        print(title)

        for stockName, pattern in combinedPatterns.items():
            if pattern.search(title) or pattern.search(body):
                mentions[stockName] += 1
                print(f"found {stockName}")
        

# Scraping multiple investing subreddits
def multiScrape(postLimit, sortingMethod, minimumMentions):
    for key in mentions.keys(): # Resets data
        mentions[key] = 0

    subreddits = ["wallstreetbets", "stockmarket", "investing", "stocks", "options",
                   "robinhood", "securityanalysis", "daytrading"]

    for subreddit in subreddits:
        getMentions(subreddit, postLimit, sortingMethod)

    mentionsFound = {}

    # Make smaller dictionary with actual found values for sorting
    for stockName in mentions:
        if mentions[stockName] >= minimumMentions:
            mentionsFound[stockName] = mentions[stockName]

    print("\n\n-RESULTS-")
    # Sorts and prints
    sortedList = dict(sorted(mentionsFound.items(), key=lambda item: item[1], reverse=True))
    for key in sortedList:
        print(f"{key}: {sortedList[key]}")
    
    return sortedList


@app.route('/mentions')
def flaskFunction():
    postLimit = int(request.args.get('postLimit'))
    sortingMethod = request.args.get('sortingMethod')
    minimumMentions = int(request.args.get('minMentions'))

    sortedDict = multiScrape(postLimit, sortingMethod, minimumMentions)
    
    stocks = []
    mentionsFound = []
 
    for key, value in sortedDict.items():
        stocks.append(key)
        mentionsFound.append(value)

    response = {"stocks": stocks, "mentions": mentionsFound}
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
