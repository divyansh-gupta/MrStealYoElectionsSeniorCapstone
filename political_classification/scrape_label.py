import json
import sys
import os
import time
import random
from pprint import pprint
path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)
import globals

fname = 'labelled.json'
with open(fname, mode='w') as f:
    json.dump([], f)

with open(fname, mode='r') as feedsjson:
    feeds = json.load(feedsjson) 

def get_tweets(screen_name):
    alltweets = []
    new_tweets = globals.api.user_timeline(screen_name = screen_name, count=200)
    if len(new_tweets) < 200:
        print ("Sn: {0} likely incorrect".format(screen_name))
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
            new_tweets = globals.api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
    return alltweets

def run(sn, label):
    try:
        tweet_list = get_tweets(sn)
    except globals.tweepy.RateLimitError as e:
        print("Rate Limit Exceeded")
        #add in a sleep here or something
        exit()
    except globals.tweepy.TweepError as e:
        print(e)
        exit()
    if len(tweet_list) > 150:
        for tweet in random.sample(tweet_list, 150):
            entry = {'text': tweet._json['text'], 'label': label }
            feeds.append(entry)
    else:
        for tweet in tweet_list:
            entry = {'text': tweet._json['text'], 'label': label }
            feeds.append(entry)
    print("Done with " + sn)
        
accs = []
with open('accounts.txt', 'r') as f:
    for line in f.read().splitlines():
        acc_name = line.split()[0]
        classif = int(line.split()[1])
        accs.append((acc_name, classif))
    
for acc in accs:
    run(acc[0], acc[1])

with open(fname, mode='w') as feedsjson:
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
