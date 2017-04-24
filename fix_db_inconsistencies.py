import pyximport; pyximport.install()
import os
import peewee
from peewee import *
from peewee import RawQuery

from rds import *
from cmain import TwitterClient

def tweet_to_dict(tweet_row):
    return {
        'tweet_text': tweet_row.tweet_text,
        'id': tweet_row.id
    }

api = TwitterClient()

redo_sentiment_tweets = RawQuery(Tweet, "select * from TWEET where TWEET.ID not in (select tweet_id from TWEETSENTIMENT);")
count = 0
sentiment_rows = []
for tweet in redo_sentiment_tweets.execute():
    sentiment_rows.append(api.get_tweet_sentiment(tweet_to_dict(tweet)))
    if count % 1000 == 0:
        print(count)
        bulk_insert_on_conflict_replace(TweetSentiment, sentiment_rows, 0)
        sentiment_rows.clear()
    count += 1
if len(sentiment_rows) > 0:
    bulk_insert_on_conflict_replace(TweetSentiment, sentiment_rows, 0)
print("Finished sentiment analysis on all unclassified tweets in db.")

# {'id': '253961531161718786', 'republican_prob': Decimal('0.44469'), 'retweet_count': 5, 'user': '565779517', 'democrat_prob': Decimal('0.44580'), 
# 'classification': 'democrat', 'third_prob': Decimal('0.10951'), 
# 'tweet_text': 'RT @bangmezarry: HARRYS NEW NUDE OMFG GUYSIM NOT KOKING ITSBSOGIG SO BITG http://t.co/hNnWpd4p', 
# 'tweet_id': '253961531161718786', 'created_at': datetime.datetime(2012, 10, 4, 20, 55, 22)}

# select count(*) from (select * from TWEET where TWEET.ID not in (select tweet_id from TWEETPOLITICAL where classification like '%\_%')) as tweets
# LEFT OUTER JOIN TWEETPOLITICAL
# ON tweets.ID = TWEETPOLITICAL.tweet_id;

def re_classify_politics():
    count = 0
    redo_political_tweets = RawQuery(Tweet, "select * from (select * from TWEET where TWEET.ID not in (select tweet_id from TWEETPOLITICAL where classification like '%%\_%%')) as tweets LEFT OUTER JOIN TWEETPOLITICAL ON tweets.ID = TWEETPOLITICAL.tweet_id;")
    political_rows = []
    for tweet in redo_political_tweets.dicts().execute():
        classified_model = api.get_political_classification_model(tweet)
        if 'republican_prob' in tweet and tweet['republican_prob'] != None:
            classified_model['republican_prob'] = tweet['republican_prob']
        if 'democrat_prob' in tweet and tweet['democrat_prob'] != None:
            classified_model['democrat_prob'] = tweet['democrat_prob']
        if 'third_prob' in tweet and tweet['third_prob'] != None:
            classified_model['third_prob'] = tweet['third_prob']
        political_rows.append(classified_model)
        if count % 1000 == 0:
            print(count)
            bulk_insert_on_conflict_replace(TweetPolitical, political_rows, 0)
            political_rows.clear()
        count += 1
    if len(political_rows) > 0:
        bulk_insert_on_conflict_replace(TweetPolitical, political_rows, 0)
    # print(political_rows)

# while True:
re_classify_politics()

print("Done reclassifying political tweets")
