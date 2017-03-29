import tweepy

auth = tweepy.OAuthHandler("***REMOVED***", "***REMOVED***")
auth.set_access_token("***REMOVED***", "***REMOVED***")

api = tweepy.API(auth)

status = api.statuses_lookup([763431268587626496])
print status