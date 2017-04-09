import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import globals
import s3
import os
import json

class TwitterClient(object):
    def __init__(self):
        tweets = []
        pass

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, parsed_tweet):
        analysis = TextBlob(self.clean_tweet(parsed_tweet['text']))
        parsed_tweet['sentiment_polarity'] = analysis.sentiment.polarity
        if analysis.sentiment.polarity > 0:
            parsed_tweet['sentiment_classification'] = 'positive'
        elif analysis.sentiment.polarity == 0:
            parsed_tweet['sentiment_classification'] = 'neutral'
        else:
            parsed_tweet['sentiment_classification'] = 'negative'

    def process_tweets(self, fetched_tweets):
        for tweet in fetched_tweets:
            self.clean_tweet(tweet)
            tweet_json = json.loads(tweet)
            parsed_tweet = {}
            parsed_tweet['text'] = tweet_json['text']
            self.get_tweet_sentiment(parsed_tweet)
            parsed_tweet['retweet_count'] = tweet_json['retweet_count']
            self.tweets.append(parsed_tweet)
            
    def get_tweets(self):
        if os.path.exists('2012_data') is False:
            os.makedirs('2012_data')
        if os.path.exists('2016_data') is False:
            os.makedirs('2016_data')

        file_key_prefix = '2012_data/cache-'

        for x in xrange(0,10):
            opened_file = ''
            file_key = file_key_prefix + str(x) + '.json'
        
            if os.path.exists(file_key) is False:
                opened_file = s3.download_from_s3('social-networking-capstone', file_key, file_key, True)
            else:
                opened_file = open(file_key, 'r')

            fetched_tweets = opened_file.readlines()
            print "File opened and read: ", file_key
            self.process_tweets(fetched_tweets)
            opened_file.close()

        return tweets

def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets()

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets: ", len(ptweets))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: ", len(ntweets))

if __name__ == "__main__":
    main()
