import globals
import pickle
import sys
import json
from pprint import pprint
classifier_file = sys.argv[1]
tweets_file = sys.argv[2]

with open(classifier_file, 'rb') as f:
    political_classifier = pickle.load(f)
    
print(political_classifier.classify("This is a fake madeup tweet"))

def load_tweets(fname):
    with open(fname,'r') as f:
        data = json.load(f)
    return data
tweet_list = load_tweets(tweets_file)

def weight_metric(tweet):
    verified = tweet['user']['verified']
    verified_wt = 0.25
    followers = tweet['user']['followers_count']
    followers_wt = 0.1
    retweets = tweet['retweet_count']
    retweets = 0.5
    favorites = tweet['user']['favourites']
    favorites_wt = 
    
for tweet in tweet_list:
    classifcation = political_classifier.classify(tweet['text'])
    tweet['classification'] = classification
    pprint(classifcation) 


    




