import json
import sys
import os
import random
import time
from pprint import pprint
#import cPickle as pickle
from textblob.classifiers import NaiveBayesClassifier
from textblob.utils import strip_punc
path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)
import constants

def split_labels(p):
	train = []
	test = []
	with open('labelled.json', 'r') as f:
		data = json.load(f)
	
	for obj in data:
		entry = (obj['text'], obj['label'])
		if random.random() <= p:
			test.append(entry)
		else:
			train.append(entry)
	
	return (train, test)
    
def save_classifier(c, fname):
    with open(fname,'wb') as f:
        pickle.dump(c, fname)

def normalize(t):
    return strip_punc(t, all=True).lower()

#removes stopwords, hyperlinks, and usernames
def get_whole_wordset(alltweets, stopwordlist):
    wordset = []
    for entry in alltweets:
        tokens = entry[0].split()
        for t in tokens:
            if t[0]=='@' or 'http' in t:
                pass
            else:
                if strip_punc(t, all=True).lower() not in stopwordlist:
                    wordset.append(strip_punc(t, all=True).lower())

    return wordset
(train, test) = split_labels(0.2)

with open('stop-word-list.txt', 'r') as f:
    stopwordlist = f.read().splitlines()
    
wordset = set(get_whole_wordset(train+test, stopwordlist))
print(len(wordset))


def custom_extractor(document, train_set):
    tokens = document.split()
    tokens = [strip_punc(t, all=True).lower() for t in tokens]
    features = dict(((u'contains({0})'.format(word), (word in tokens))
                                            for word in wordset))

    return features

print(len(train))
start = time.time()
cl = NaiveBayesClassifier(train, feature_extractor=custom_extractor)
end = time.time()
elapsed = end - start

print('Took {0} seconds to classify {1} tweets'.format(str(elapsed), str(len(train))))

cl.show_informative_features()

print(cl.accuracy(test))