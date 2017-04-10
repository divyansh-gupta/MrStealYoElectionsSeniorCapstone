import os
import json
from tweepy import OAuthHandler
from textblob import TextBlob
from multiprocessing.dummy import Pool

import globals
import s3
from rds import *

class TwitterClient(object):
    def __init__(self):
        self.clean_tweet = globals.clean_tweet
        self.twitter_time_to_datetime = globals.twitter_time_to_datetime
        self.file_key_prefix = '2012_data/cache-'

    def get_tweet_sentiment(self, tweet_model):
        analysis = TextBlob(self.clean_tweet(tweet_model['tweet_text']))
        tweet_sentiment_model = { 
            'tweet': tweet_model['id'],
            'polarity': analysis.sentiment.polarity
        }
        if analysis.sentiment.polarity > 0:
            tweet_sentiment_model['classification'] = 'positive'
        elif analysis.sentiment.polarity == 0:
            tweet_sentiment_model['classification'] = 'neutral'
        else:
            tweet_sentiment_model['classification'] = 'negative'
        return tweet_sentiment_model

    def get_user_model(self, user_json):
        user_model = {
            'id': user_json['id_str'],
            'followers_count': user_json['followers_count'],
            'friends_count': user_json['friends_count'],  
            'location': user_json['location'],
            'name': user_json['name'],
            'screen_name': user_json['screen_name'],
            'statuses_count': user_json['statuses_count'],
            'verified': user_json['verified'] 
        }
        return user_model

    def get_hashtag_models(self, hashtag_models, tweet_id, hashtags_json_array):
        hashtag_count = len(hashtags_json_array)
        for x in xrange(0, hashtag_count):
            hashtag_model = {
                'tweet': tweet_id,
                'hashtag': hashtags_json_array[x]['text'].lower()
            }
            hashtag_models.append(hashtag_model)

    def insert_all_information_into_db(self, user_models, tweet_models, tweet_sentiment_models, hashtag_models):
        print "inserting users, size: ", len(user_models.values())
        bulk_insert_on_conflict_replace(User, user_models.values())
        print "inserting tweets, size: ", len(tweet_models)
        bulk_insert_on_conflict_replace(Tweet, tweet_models)
        print "inserting tweet sentiments, size: ", len(tweet_sentiment_models)
        bulk_insert_on_conflict_replace(TweetSentiment, tweet_sentiment_models)
        print "inserting hashtags, size: ", len(hashtag_models)
        bulk_insert_on_conflict_replace(HashTag, hashtag_models)

    def process_tweets(self, fetched_tweets):
        user_models = {}
        tweet_sentiment_models = []
        hashtag_models = []
        def process_tweet(tweet):
            tweet_json = json.loads(tweet)
            tweet_model = {
                'tweet_text': tweet_json['text'],
                'id': tweet_json['id_str'],
                'created_at': self.twitter_time_to_datetime(tweet_json['created_at']),
                'retweet_count': tweet_json['retweet_count']
            }
            tweet_sentiment_models.append(self.get_tweet_sentiment(tweet_model))
            user_model = self.get_user_model(tweet_json['user'])
            tweet_model['user'] = user_model['id']
            user_models[user_model['id']] = user_model
            self.get_hashtag_models(hashtag_models, tweet_model['id'], tweet_json['entities']['hashtags'])
            return tweet_model
        print "starting tweet processing"
        tweet_models = map(process_tweet, fetched_tweets)
        self.insert_all_information_into_db(user_models, tweet_models, tweet_sentiment_models, hashtag_models)
            
    def get_and_process_tweets(self, x):
        opened_file = ''
        file_key = self.file_key_prefix + str(x) + '.json'
    
        if os.path.exists(file_key) is False:
            opened_file = s3.download_from_s3('social-networking-capstone', file_key, file_key, True)
        else:
            opened_file = open(file_key, 'r')

        fetched_tweets = opened_file.readlines()
        print "File opened and read: ", file_key
        self.process_tweets(fetched_tweets)
        opened_file.close()

def top_level_get_and_process_tweets(x):
    api = TwitterClient()
    api.get_and_process_tweets(x)

def main():
    if os.path.exists('2012_data') is False:
        os.makedirs('2012_data')
    if os.path.exists('2016_data') is False:
        os.makedirs('2016_data')

    pool = Pool()

    files_to_process = xrange(0, 10)
    pool.map(top_level_get_and_process_tweets, files_to_process)

    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
