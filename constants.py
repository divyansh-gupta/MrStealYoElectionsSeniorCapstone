from enum import Enum
import tweepy
class Classifications(Enum):
	democrat = 1
	republican = 2
	third = 3
auth = tweepy.OAuthHandler("***REMOVED***", "***REMOVED***")
auth.set_access_token("***REMOVED***", "***REMOVED***")
api = tweepy.API(auth)
