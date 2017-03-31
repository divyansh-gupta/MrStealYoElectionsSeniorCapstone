import json
import sys
import os
from pprint import pprint
path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)
import constants

tweet_list = [{"text": "this is a democratic tweet"}, {"text": "this is another democratic tweet"}]

label = constants.Classifications.democrat

fname = 'labelled.json'
if not os.path.isfile(fname):
    with open(fname, mode='w', encoding='utf-8') as f:
        json.dump([], f)

with open(fname, mode='r', encoding='utf-8') as feedsjson:
    feeds = json.load(feedsjson) 

for tweet in tweet_list:
    entry = {'text': tweet['text'], 'label':label.value}
    feeds.append(entry)
    
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
