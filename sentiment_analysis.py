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
        pass

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self):
        tweets = []

        if os.path.exists('2012_data') is False:
            os.makedirs('2012_data')
        if os.path.exists('2016_data') is False:
            os.makedirs('2016_data')

        file_key = '2012_data/cache-0.json'
        opened_file = ''
        if os.path.exists(file_key) is False:
            opened_file = s3.download_from_s3('social-networking-capstone', file_key, file_key, True)
        else:
            opened_file = open(file_key, 'r')
        fetched_tweets = opened_file.readlines()

        print "File has been opened and read."

        for tweet in fetched_tweets:
            # empty dictionary to store required params of a tweet
            self.clean_tweet(tweet)
            tweet_json = json.loads(tweet)
            parsed_tweet = {}

           # saving text of tweet
            parsed_tweet['text'] = tweet_json['text']
            # saving sentiment of tweet
            parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet_json['text'])
            tweets.append(parsed_tweet)

            # appending parsed tweet to tweets list
            # if tweet.retweet_count > 0:
            #     # if tweet has retweets, ensure that it is appended only once
            #     if parsed_tweet not in tweets:
            #         tweets.append(parsed_tweet)
            # else:
            #     tweets.append(parsed_tweet)

        # return parsed tweets
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
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    main()
