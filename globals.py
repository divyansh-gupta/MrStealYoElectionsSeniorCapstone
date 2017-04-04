from enum import Enum
import tweepy
from textblob.classifiers import NaiveBayesClassifier
from textblob.utils import strip_punc
class Classifications(Enum):
	democrat = 1
	republican = 2
	third = 3
    
class Pclassifier:
    def __init__(self, filename, wordset):
        self.filename = filename
        self.wordset = wordset
        self.classifier = None
        
    def normalize(self, t):
        return strip_punc(t, all=True).lower()
    
    def custom_extractor(self, document, train_set):
        tokens = document.split()
        tokens = [self.normalize(t) for t in tokens]
        features = dict(((u'contains({0})'.format(word), (word in tokens))
                                            for word in self.wordset))
        return features
    
    def train(self, train_set):
        self.classifier = NaiveBayesClassifier(train_set, self.custom_extractor)
    
    def classify(self, text):
        self.classifier.classify(text)
    
    def notable_features(self):
        self.classifier.show_informative_features()
        
    def test(self, test_set):
        print(self.classifier.accuracy(test_set))    
    
auth = tweepy.OAuthHandler("***REMOVED***", "***REMOVED***")
auth.set_access_token("***REMOVED***", "***REMOVED***")
api = tweepy.API(auth)
