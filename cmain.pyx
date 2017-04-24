import os
import json
import pickle
from textblob import TextBlob
from multiprocessing import Pool

import globals
import s3
from rds import *

class TwitterClient(object):
    def __init__(self):
        self.clean_tweet = globals.clean_tweet
        self.twitter_time_to_datetime = globals.twitter_time_to_datetime
        self.file_key_prefix = '2012_data/cache-'
        self.classifier_file_name = 'c2.classifier'
        self.i = 0
        self.every_100th = 0
        if os.path.exists(self.classifier_file_name) is False:
            print('downloading classifier file from s3')
            s3.download_from_s3('social-networking-capstone', self.classifier_file_name, self.classifier_file_name, True)
        print("loading classifier")
        classifier_file = open(self.classifier_file_name, 'rb')
        self.pclassifier = pickle.load(classifier_file)
        classifier_file.close()
        print('classifier loaded')

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

    def get_political_classification_model(self, tweet_model):
        classification = self.pclassifier.classify(tweet_model['tweet_text'])
        political_classification_model = {
            'tweet': tweet_model['id'],
            'democrat_prob': 0.00,
            'republican_prob': 0.00,
            'third_prob': 0.00,
            'classification': classification
        }
        return political_classification_model

    def get_hashtag_models(self, hashtag_models, tweet_id, hashtags_json_array):
        hashtag_count = len(hashtags_json_array)
        for x in range(0, hashtag_count):
            hashtag_model = {
                'tweet': tweet_id,
                'hashtag': hashtags_json_array[x]['text'].lower()
            }
            hashtag_models.append(hashtag_model)

    def insert_all_information_into_db(self, user_models, tweet_models, tweet_sentiment_models, hashtag_models, political_classification_models):
        print("inserting users, size: " + str(len(user_models.values())))
        bulk_insert_on_conflict_replace(User, user_models.values(), 0)
        print ("inserting tweets, size: " + str(len(tweet_models)))
        bulk_insert_on_conflict_replace(Tweet, tweet_models, 0)
        print ("inserting tweet sentiments, size: " + str(len(tweet_sentiment_models)))
        bulk_insert_on_conflict_replace(TweetSentiment, tweet_sentiment_models, 0)
        print ("inserting hashtags, size: " + str(len(hashtag_models)))
        bulk_insert_on_conflict_replace(HashTag, hashtag_models, 0)
        print ("inserting political classification, size: " + str(len(political_classification_models)))
        bulk_insert_on_conflict_replace(TweetPolitical, political_classification_models, 0)

    def process_tweets(self, fetched_tweets):
        user_models = {}
        tweet_models = []
        tweet_sentiment_models = []
        hashtag_models = []
        political_classification_models = []
        def process_tweet(tweet):
            self.every_100th += 1
            if (self.every_100th % 50 != 0):
                return "null"
            tweet_json = json.loads(tweet)
            try:
                tweet_model = {
                    'tweet_text': tweet_json['text'],
                    'id': tweet_json['id_str'],
                    'created_at': self.twitter_time_to_datetime(tweet_json['created_at']),
                    'retweet_count': tweet_json['retweet_count']
                }
            except Exception as e:
                self.every_100th -= 1
                print("Some expected keyvalue didn't exist")
                return "null"
            tweet_sentiment_models.append(self.get_tweet_sentiment(tweet_model))
            user_model = self.get_user_model(tweet_json['user'])
            tweet_model['user'] = user_model['id']
            user_models[user_model['id']] = user_model
            self.get_hashtag_models(hashtag_models, tweet_model['id'], tweet_json['entities']['hashtags'])
            political_classification_models.append(self.get_political_classification_model(tweet_model))
            tweet_models.append(tweet_model)
        print("starting tweet processing")
        fetched_tweets_len = len(fetched_tweets)
        for x in range(0, fetched_tweets_len):
            process_tweet(fetched_tweets[x])
        print("processing of tweets done")
        self.insert_all_information_into_db(user_models, tweet_models, tweet_sentiment_models, hashtag_models, political_classification_models)

    def get_and_process_tweets(self, x):
        opened_file = ''
        file_key = self.file_key_prefix + str(x) + '.json'

        if os.path.exists(file_key) is False:
            opened_file = s3.download_from_s3('social-networking-capstone', file_key, file_key, True)
        else:
            opened_file = open(file_key, 'r')

        fetched_tweets = opened_file.readlines()
        print("File opened and read: " + file_key)
        self.process_tweets(fetched_tweets)
        opened_file.close()