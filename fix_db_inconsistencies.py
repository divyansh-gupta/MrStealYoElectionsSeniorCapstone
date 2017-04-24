import pyximport; pyximport.install()
import os
import peewee

from rds import *
from cmain import TwitterClient

def tweet_to_dict(tweet_row):
    return {
        'tweet_text': tweet_row.tweet_text,
        'id': tweet_row.id
    }

api = TwitterClient()

i = 0
for tweet_row in Tweet.select():
    try:
        sentiment_rows = TweetSentiment.select(TweetSentiment.tweet == tweet_row.id)
        print sentiment_rows
    except Exception as e:
        print("Sentiment row doesn't exist")
        bulk_insert_on_conflict_replace(TweetSentiment, [api.get_tweet_sentiment(tweet_to_dict(tweet_row))])
    print(i)
    i += 1