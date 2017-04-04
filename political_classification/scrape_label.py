import json
import sys
import os
import time
import random
from pprint import pprint
path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)
import constants

max_tweets = 800

fname = 'labelled.json'
if not os.path.isfile(fname):
    with open(fname, mode='w', encoding='utf-8') as f:
        json.dump([], f)

with open(fname, mode='r', encoding='utf-8') as feedsjson:
    feeds = json.load(feedsjson) 

def get_tweets(screen_name):
    alltweets = []
    new_tweets = constants.api.user_timeline(screen_name = screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(alltweets) < max_tweets:
            new_tweets = constants.api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
    return alltweets

def run(sn, label):
    try:
        tweet_list = get_tweets(sn)
    except constants.tweepy.RateLimitError as e:
        print("Rate Limit Exceeded")
        #add in a sleep here or something
        exit()
    except constants.tweepy.TweepError as e:
        print(e)
        exit()
    for tweet in tweet_list:
        entry = {'text': tweet._json['text'], 'label':label.value}
        feeds.append(entry)
    print("Done with " + sn)
        
run('RealDonaldTrump', constants.Classifications.republican)
run('BernieSanders', constants.Classifications.democrat)
run('BarackObama', constants.Classifications.democrat)
run('SpeakerRyan', constants.Classifications.republican)
run('SenJohnMcCain', constants.Classifications.republican)

with open(fname, mode='w', encoding='utf-8') as feedsjson:
    try:
        json.dump(feeds, feedsjson)
    except IOError as e:
        pprint ("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
        pprint ("Could not convert data to an integer.")
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
exit()