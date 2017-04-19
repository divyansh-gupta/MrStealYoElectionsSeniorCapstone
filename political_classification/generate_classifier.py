import json
import sys
import os
import random
import time
from pprint import pprint
import pickle
path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)
import globals

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
        pickle.dump(c, f)

def normalize(t):
    return globals.strip_punc(t, all=True).lower()

#removes stopwords, hyperlinks, and usernames
def get_whole_wordset(alltweets, stopwordlist):
    wordset = {}
    for entry in alltweets:
        tokens = entry[0].split()
        for t in tokens:
            normalized = normalize(t)
            if '@' in t or 'http' in t or len(t) < 3:
                pass
            else:
                if normalized not in stopwordlist:
                    if normalized not in wordset:
                        wordset[normalized] = 0
                    else:
                        wordset[normalized]+=1
    s = [(k, wordset[k]) for k in sorted(wordset, key=wordset.get, reverse=True)]
    return [k for k,v in s]
(train, test) = split_labels(0.1)

with open('stop-word-list.txt', 'r') as f:
    stopwordlist = f.read().splitlines()
    
wordset = get_whole_wordset(train+test, stopwordlist)

wordset = wordset[0:int(len(wordset)*.7)]
print(len(wordset))

print(len(train))
start = time.time()
pclass = globals.Pclassifier('c1.classifier', wordset)
pclass.train(train)
end = time.time()
elapsed = end - start

print('Took {0} seconds to classify {1} tweets'.format(str(elapsed), str(len(train))))

#pclass.notable_features()

#print(pclass.classifier.pretty_format())

pclass.test(test)

with open(pclass.filename, 'wb') as f:
    pickle.dump(pclass, f)