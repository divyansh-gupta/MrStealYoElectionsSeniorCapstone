from rds import *
import peewee

i = 0
for tweet_row in Tweet.select():
	sentiment_row = TweetSentiment.get(TweetSentiment.tweet == tweet_row.ID)
	print(sentiment_row)
	i += 1