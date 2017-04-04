import globals
import pickle
import sys

classifier_file = sys.argv[1]
tweets_file = sys.argv[2]

with open(classifier_file, 'rb') as f:
    political_classifier = pickle.load(f)
    
print(political_classifier.classify("This is a fake madeup tweet"))


