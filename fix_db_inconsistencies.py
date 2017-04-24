import pyximport; pyximport.install()
import os
import peewee
from peewee import *

from rds import *
from cmain import TwitterClient

def tweet_to_dict(tweet_row):
    return {
        'tweet_text': tweet_row.tweet_text,
        'id': tweet_row.id
    }

rq = RawQuery(TWEET, 'select * from TWEET where TWEET.ID not in (select tweet_id from TWEETSENTIMENT);')

count = 0
for obj in rq.execute():
    count += 1
print(count)
print(obj[0])

# api = TwitterClient()




# i = 0
# for tweet_row in Tweet.select():
#     try:
#         sentiment_rows = TweetSentiment.select(TweetSentiment.tweet == tweet_row.id)
#         print sentiment_rows
#     except Exception as e:
#         print("Sentiment row doesn't exist")
#         bulk_insert_on_conflict_replace(TweetSentiment, [api.get_tweet_sentiment(tweet_to_dict(tweet_row))])
#     print(i)
#     i += 1