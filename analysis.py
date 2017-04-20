from rds import *
import pickle
import matplotlib.pyplot as plt
import sys

def get_tweets():
    database.connect()

    tweet_query = (Tweet.select(Tweet, TweetPolitical, TweetSentiment, User)
    .join(TweetPolitical)
    .where(TweetPolitical.tweet == Tweet.id)
    .switch(Tweet)
    .join(TweetSentiment)
    .where(TweetSentiment.tweet == Tweet.id)
    .switch(Tweet)
    .join(User)
    .naive())


    results = tweet_query.execute()
    database.close()

    list_tweets = []
    for result in results:
        list_tweets.append(result)
    return list_tweets

def save_sample_set(days):
    sample_tweet_list = []
    for k in days:
        sample_tweet_list.extend(days[k][0:500])
    pickle_tweets(sample_tweet_list[:-500], sample_fname)

def pickle_tweets(tweet_list, fname):
    with open(fname, 'wb') as f:
        pickle.dump(tweet_list, f)

def unpickle_tweets(fname):
    list_tweets = []
    with open(fname, 'rb') as f:
        list_tweets = pickle.load(f)
    return list_tweets

def percent_positive(tweet_list):
    pos_count = 0
    for tweet in tweet_list:
        if tweet.classification == 'positive':
            pos_count+= 1
    return float(pos_count/len(tweet_list))

def in_days(tweet_list):
    days = {}
    for tweet in tweet_list:
        key = str(tweet.created_at.date())
        if key not in days:
            days[key] = []
        days[key].append(tweet)
    return days

def in_months(tweet_list):
    months = {}
    for tweet in tweet_list:
        key = '{0}-{1}'.format(str(tweet.created_at.month), str(tweet.created_at.year))
        if key not in months:
            months[key] = []
        months[key].append(tweet)
    return months

def in_locations(tweet_list):
    locations = {}
    for tweet in tweet_list:
        key = tweet.location
        if key not in locations:
            locations[key] = []
            locations[key].append(tweet)
    return locations

def day_to_number(day_str):
    return int(day_str.replace('-',''))

def plot_percent_positive_per_day(days):
    x = [day_to_number(k) for k in list(days.keys())]
    y = [percent_positive(days[k]) for k in days]
    plt.figure()
    plt.plot(x, y)
    plt.xticks(x, [str(xi) for xi in x])
    plt.show()

#returns 'r' 'd' or 't'
def pclassification(tweet):
    d = {'r': tweet.republican_prob, 'd': tweet.democrat_prob, 't': tweet.third_prob}
    return max(d, key=d.get)

def percent_political_classifcation(tweet_list):
    rep_count = 0
    dem_count = 0
    thr_count = 0
    for tweet in tweet_list:
        classif = pclassification(tweet)
        if classif == 'r':
            rep_count += 1
        elif classif =='d':
            dem_count +=1
        else:
            thr_count +=1
    total_tweets = len(tweet_list)
    return (float(rep_count/total_tweets), float(dem_count/total_tweets), float(thr_count/total_tweets))

def percent_political(tweet_list):
    rep_probabilities = 0
    dem_probabilities = 0
    thr_probabilities = 0
    for tweet in tweet_list:
        rep_probabilities += tweet.republican_prob
        dem_probabilities += tweet.democrat_prob
        thr_probabilities += tweet.third_prob
    total_tweets = len(tweet_list)
    return (float(rep_probabilites/total_tweets), float(dem_probabilites/total_tweets), float(thr_probabilites/total_tweets))

def plot_percent_pclassification_per_day(days):
    x = [day_to_number(k) for k in list(days.keys())]
    yr = []
    yd = []
    yt = []
    for k in days:
        pclasses = percent_political_classifcation(days[k])
        yr.append(pclasses[0])
        yd.append(pclasses[1])
        yt.append(pclasses[2])

    fig, ax = plt.subplots()
    ax.plot(x, yr, label="Republican")
    ax.plot(x, yd, label="Democrat")
    ax.plot(x, yt, label="Third Party")
    ax.legend(loc='upper right')
    plt.xticks(x, [str(xi) for xi in x])

    plt.show()

def plot_percent_pclassification_probs_per_day(days):
    x = [day_to_number(k) for k in list(days.keys())]
    yr = []
    yd = []
    yt = []
    for k in days:
        pclasses = percent_political(days[k])
        yr.append(pclasses[0])
        yd.append(pclasses[1])
        yt.append(pclasses[2])

    fig, ax = plt.subplots()
    ax.plot(x, yr, label="Republican")
    ax.plot(x, yd, label="Democrat")
    ax.plot(x, yt, label="Third Party")
    ax.legend(loc='upper right')
    plt.xticks(x, [str(xi) for xi in x])

    plt.show()

pull_from_db = False
try:
    if sys.argv[1] == 'pull':
        pull_from_db = True
except:
    print('Usage: python analysis.py <num_tweets> <pull?>')
    exit()

list_tweets = []
fname = 'tweet_list.pickle'
sample_fname = 'sample_tweet_list.pickle'

if pull_from_db:
    start = time.time()
    list_tweets = get_tweets()
    end = time.time()
    elapsed = end - start
    print('Took {0} seconds to pull {1} tweets'.format(str(elapsed), len(list_tweets)))
    pickle_tweets(list_tweets, fname)
else:
    list_tweets = unpickle_tweets(sample_fname)

days = in_days(list_tweets)


# locs = in_locations(list_tweets)
# for k in locs:
#     print ('Location: {0} has {1} tweets'.format(k, len(locs[k])))

#plot_percent_pclassification_per_day(days)
#plot_percent_pclassification_probs_per_day(days)
#for k in days:
#    print ('Day: {0} has {1} tweets'.format(k, len(days[k])))
#plot_percent_positive_per_day(days)
