from rds import *
import pickle

def get_tweets(limit):
    database.connect()

    tweet_query = (Tweet.select(Tweet, TweetPolitical, TweetSentiment)
    .limit(limit)
    .join(TweetPolitical)
    .where(TweetPolitical.tweet == Tweet.id)
    .switch(Tweet)
    .join(TweetSentiment)
    .where(TweetSentiment.tweet == Tweet.id)
    .naive()
    .order_by(Tweet.created_at.desc()))

    #takes significant time
    results = tweet_query.execute()
    database.close()

    list_tweets = []
    for result in results:
        list_tweets.append(result)
    return list_tweets

def pickle_tweets(tweet_list):
    with open('tweet_list.pickle', 'wb') as f:
        pickle.dump(tweet_list, f)

def unpickle_tweets():
    list_tweets = []
    with open('tweet_list.pickle', 'rb') as f:
        list_tweets = pickle.load(f)

list_tweets = get_tweets(50)
#pickle_tweets(list_tweets)

print(list_tweets[10].tweet_text)
print(list_tweets[10].classification)
