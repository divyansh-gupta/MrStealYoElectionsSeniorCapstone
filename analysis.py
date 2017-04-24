import pickle
import matplotlib.pyplot as plt
import sys
import MySQLdb
import peewee
import datetime
import time
from peewee import *
import random
import json
import globals


actual_electoral_votes = {
"AL": {
  "class": "r",
  "votes": 9
 },
"AK": {
  "class": "r",
  "votes": 3
 },
"AZ": {
  "class": "r",
  "votes": 11
 },
"AR": {
  "class": "r",
  "votes": 6
 },
"CA": {
  "class": "d",
  "votes": 55
 },
"CO": {
  "class": "d",
  "votes": 9
 },
"CT": {
  "class": "d",
  "votes": 7
 },
"DE": {
  "class": "d",
  "votes": 3
 },
"DC": {
  "class": "d",
  "votes": 3
 },
"FL": {
  "class": "d",
  "votes": 29
 },
"GA": {
  "class": "r",
  "votes": 16
 },
"HI": {
  "class": "d",
  "votes": 4
 },
"ID": {
  "class": "r",
  "votes": 4
 },
"IL": {
  "class": "d",
  "votes": 20
 },
"IN": {
  "class": "r",
  "votes": 11
 },
"IA": {
  "class": "d",
  "votes": 6
 },
"KS": {
  "class": "r",
  "votes": 6
 },
"KY": {
  "class": "r",
  "votes": 8
 },
"LA": {
  "class": "r",
  "votes": 8
 },
"ME": {
  "class": "d",
  "votes": 4
 },
"MD": {
  "class": "d",
  "votes": 10
 },
"MA": {
  "class": "d",
  "votes": 11
 },
"MI": {
  "class": "d",
  "votes": 16
 },
"MN": {
  "class": "d",
  "votes": 10
 },
"MS": {
  "class": "r",
  "votes": 6
 },
"MO": {
  "class": "r",
  "votes": 10
 },
"MT": {
  "class": "r",
  "votes": 3
 },
"NE": {
  "class": "r",
  "votes": 5
 },
"NV": {
  "class": "d",
  "votes": 6
 },
"NH": {
  "class": "d",
  "votes": 4
 },
"NJ": {
  "class": "d",
  "votes": 14
 },
"NM": {
  "class": "d",
  "votes": 5
 },
"NY": {
  "class": "d",
  "votes": 29
 },
"NC": {
  "class": "r",
  "votes": 15
 },
"ND": {
  "class": "r",
  "votes": 3
 },
"OH": {
  "class": "d",
  "votes": 18
 },
"OK": {
  "class": "r",
  "votes": 7
 },
"OR": {
  "class": "d",
  "votes": 7
 },
"PA": {
  "class": "d",
  "votes": 20
 },
"RI": {
  "class": "d",
  "votes": 4
 },
"SC": {
  "class": "r",
  "votes": 9
 },
"SD": {
  "class": "r",
  "votes": 3
 },
"TN": {
  "class": "r",
  "votes": 11
 },
"TX": {
  "class": "r",
  "votes": 38
 },
"UT": {
  "class": "r",
  "votes": 6
 },
"VT": {
  "class": "d",
  "votes": 3
 },
"VA": {
  "class": "d",
  "votes": 13
 },
"WA": {
  "class": "d",
  "votes": 12
 },
"WV": {
  "class": "r",
  "votes": 5
 },
"WI": {
  "class": "d",
  "votes": 10
 },
"WY": {
  "class": "r",
  "votes": 3
 }
 }

state_dict = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}


database = MySQLDatabase (
    'socialnetworkingdb',
    **{
        'host': '***REMOVED***',
        'password': '***REMOVED***',
        'user': '***REMOVED***'
     }
)

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    id = CharField(db_column='ID', primary_key=True)
    followers_count = IntegerField()
    friends_count = IntegerField()
    location = CharField(null=True)
    name = CharField()
    screen_name = CharField()
    statuses_count = IntegerField()
    verified = IntegerField()

    class Meta:
        db_table = 'USER'

class Tweet(BaseModel):
    id = CharField(db_column='ID', primary_key=True)
    created_at = DateTimeField(null=True)
    retweet_count = IntegerField()
    tweet_text = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=User, to_field='id')

    class Meta:
        db_table = 'TWEET'

class HashTag(BaseModel):
    hashtag = CharField()
    tweet = ForeignKeyField(db_column='tweet_id', rel_model=Tweet, to_field='id')

    class Meta:
        db_table = 'HASHTAG'
        indexes = (
            (('tweet', 'hashtag'), True),
        )
        primary_key = CompositeKey('hashtag', 'tweet')

class TweetSentiment(BaseModel):
    classification = CharField()
    polarity = DecimalField()
    tweet = ForeignKeyField(db_column='tweet_id', primary_key=True, rel_model=Tweet, to_field='id')

    class Meta:
        db_table = 'TWEETSENTIMENT'

class TweetPolitical(BaseModel):
    classification = CharField()
    democrat_prob = DecimalField()
    republican_prob = DecimalField()
    third_prob = DecimalField()
    tweet = ForeignKeyField(db_column='tweet_id', primary_key=True, rel_model=Tweet, to_field='id')

    class Meta:
        db_table = 'TWEETPOLITICAL'

def get_maxes(tweet_list):
    MAX_RTS = 0
    MAX_FOLLOWERS = 0
    for tweet in tweet_list:
        if tweet.retweet_count > MAX_RTS:
            MAX_RTS = tweet.retweet_count
        if tweet.followers_count > MAX_FOLLOWERS:
            MAX_FOLLOWERS = tweet.followers_count
    print('{0} max rts, {1} max followers'.format(MAX_RTS, MAX_FOLLOWERS))
    return (MAX_RTS, MAX_FOLLOWERS)

def get_all_tweets(limit):
    database.connect()

    tweet_query = (Tweet.select(Tweet, TweetPolitical, TweetSentiment, User)
    .join(TweetPolitical)
    .where(TweetPolitical.tweet == Tweet.id)
    .switch(Tweet)
    .join(TweetSentiment)
    .where(TweetSentiment.tweet == Tweet.id)
    .switch(Tweet)
    .join(User)
    .limit(1000000)
    .naive())

    results = tweet_query.execute()
    database.close()

    list_tweets = []
    for result in results:
        list_tweets.append(result)
    return list_tweets

def tweets_with_hashtag_to_labelled(hashtag, label):
    database.connect()

    tweet_query = (HashTag.select(HashTag, Tweet, TweetPolitical, TweetSentiment, User)
    .where(fn.Lower(HashTag.hashtag) == hashtag)
    .join(Tweet)
    .join(TweetPolitical)
    .where(TweetPolitical.tweet == Tweet.id)
    .switch(Tweet)
    .join(TweetSentiment)
    .where(TweetSentiment.tweet == Tweet.id)
    .switch(Tweet)
    .join(User)
    .limit(8000)
    .naive())

    results = tweet_query.execute()
    database.close()

    list_tweets = []
    for result in results:
        list_tweets.append({'text': result.tweet_text, 'label': label})
    return list_tweets

def get_tweets_with_hashtag(hashtag, limit):
    database.connect()

    tweet_query = (HashTag.select(HashTag, Tweet, TweetPolitical, TweetSentiment, User)
    .limit(limit)
    .where(fn.Lower(HashTag.hashtag) == hashtag)
    .join(Tweet)
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

def get_tweets_nth_row(n, limit):
    database.connect()

    tweet_query = (Tweet.select(Tweet, TweetPolitical, TweetSentiment, User)
    .limit(limit)
    .where(Tweet.id % n == 0)
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

### Tweet Bucket Methods ###
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

def get_normalize_days(tweet_list, tweets_per_day):
    days = in_days(tweet_list)
    start = time.time()
    for k in days:
        if len(days[k]) > tweets_per_day :
            days[k] = random.sample(days[k], tweets_per_day)
    end = time.time()
    elapsed = end - start
    print('Took {0} to sample {1} tweets per day for {2} days'.format(elapsed, tweets_per_day, len(days)))
    return days

def in_states(tweet_list):
    #state list as kv pair, state_list[abbrv] = full-state-name
    states = {}
    for tweet in tweet_list:
        for k in state_dict:
            if tweet.location is None:
                pass
            elif k in tweet.location.split() or state_dict[k] in tweet.location:
                if k not in states:
                    states[k] = []
                states[k].append(tweet)
    return states

### End Bucket Methods ###

### Metrics
def political_lean(pdict, sentiment_polarity):
    polit = 1 if (pdict['1'] > pdict['2']) == 1 else -1
    prob = abs(pdict['1'] - pdict['2'])
    return float(polit) * float(prob)


def togetherness(prob1, prob2, prob3):
    return 1 - max(abs(prob1-prob2), abs(prob1-prob3), abs(prob2-prob3))

def weight(tweet, MAX_RTS, MAX_FOLLOWERS):
    return (0.35 * tweet.verified +
            0.2 * float(tweet.retweet_count/MAX_RTS) +
            0.45 * float(tweet.followers_count/MAX_FOLLOWERS))

def day_to_number(day_str):
    return int(day_str.replace('-',''))

def percent_positive(tweet_list):
    pos_count = 0
    for tweet in tweet_list:
        if tweet.classification == 'positive':
            pos_count+= 1
    return float(pos_count/len(tweet_list))

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

def sentiments(tweet_list):
    pos_count = 0
    neg_count = 0
    neut_count = 0
    for tweet in tweet_list:
        if tweet.classification == 'positive':
            pos_count+= 1
        elif tweet.classification == 'negative':
            neg_count+=1
        else:
            neut_count +=1
    return (float(pos_count/len(tweet_list)), float(neg_count/len(tweet_list)), float(neut_count/len(tweet_list)))

def percent_political(tweet_list):
    rep_probabilities = 0
    dem_probabilities = 0
    thr_probabilities = 0
    for tweet in tweet_list:
        rep_probabilities += tweet.republican_prob
        dem_probabilities += tweet.democrat_prob
        thr_probabilities += tweet.third_prob
    total_tweets = len(tweet_list)
    return (float(rep_probabilities/total_tweets), float(dem_probabilities/total_tweets), float(thr_probabilities/total_tweets))

#higher negative = higher republican
def political_score(tweet_list, MAX_RTS, MAX_FOLLOWERS):
    score = 0
    for tweet in tweet_list:
        wt = weight(tweet, MAX_RTS, MAX_FOLLOWERS)
        sent = -1 if tweet.classification == 'negative' else 1
        pclass_mod = 1 if pclassification(tweet) == 'd' else -1
        #pprob = tweet.republican_prob if pclass_mod == -1 else tweet.democrat_prob
        score += float(wt * sent * pclass_mod)
    return float(score/len(tweet_list))

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

def plot_percent_positive_per_day(days):
    x = [day_to_number(k) for k in list(days.keys())]
    y = [percent_positive(days[k]) for k in days]
    plt.figure()
    plt.plot(range(len(x)), y)
    plt.xticks(range(len(x)), [str(xi) for xi in x], rotation = 'vertical')
    plt.show()

def plot_togetherness(days):
    x = [day_to_number(k) for k in list(days.keys())]
    y = []
    for k in days:
        (rprob, dprob, tprob) = percent_political(days[k])
        y.append(togetherness(rprob, dprob, tprob))
    plt.figure()
    plt.title("Togetherness Metric over time")
    plt.plot(range(len(x)), y)
    x_strs = [str(xi) for xi in x]
    plt.xticks(range(len(x)), x_strs)
    plt.show()

def state_analysis(list_tweets):
    states = in_states(list_tweets)
    state_probs = {}
    for k in states:
        (rper, dper, tper) = percent_political_classifcation(states[k])
        d = {'r': rper, 'd': dper, 't': tper}
        classif = max(d, key=d.get)
        state_probs[k] = {'r': rper, 'd': dper, 't': tper, 'class': classif}


    num_incorrect = 0
    electoral_votes_incorrect = 0
    for k in states:
        if actual_electoral_votes[k]['class'] != state_probs[k]['class']:
            num_incorrect+= 1
            electoral_votes_incorrect += actual_electoral_votes[k]['votes']
            print('State {0} incorrect, rep_prob: {1}, dem_prob: {2}'.format(k, state_probs[k]['r'], state_probs[k]['d']))
    accuracy = 1 - float(num_incorrect/len(states))
    accuracy_electoral = float((538-electoral_votes_incorrect)/538)
    print('Model State Electoral Vote Prediction Accuracy by Votes: {0}, {1}/538 votes correct'.format(accuracy_electoral, 538-electoral_votes_incorrect))
    print('Model State Electoral Vote Prediction Accuracy by States: {0}, {1}/{2} states correct'.format(accuracy, len(states)-num_incorrect, len(states)))
    sort_repub = [k for k in sorted(state_probs, key=lambda s:state_probs[s]['r'], reverse=True)]
    sort_dem = [k for k in sorted(state_probs, key=lambda s:state_probs[s]['d'], reverse=True)]
    print('10 most republican states: ', sort_repub[0:10])
    print('10 most democrat states: ', sort_dem[0:10])

def plot_percent_positve_and_classifications(days):
    x = [day_to_number(k) for k in list(days.keys())]
    y = [percent_positive(days[k]) for k in days]

    yr = []
    yd = []
    yt = []
    for k in days:
        pclasses = percent_political_classifcation(days[k])
        yr.append(pclasses[0])
        yd.append(pclasses[1])
        yt.append(pclasses[2])

    fig, ax = plt.subplots()
    ax.plot(range(len(x)), y, label='Percent Positive')
    ax.plot(range(len(x)), yr, label="Republican")
    ax.plot(range(len(x)), yd, label="Democrat")
    ax.plot(range(len(x)), yt, label="Third Party")
    ax.legend(loc='upper right')
    plt.xticks(range(len(x)), [str(xi) for xi in x])
    plt.show()

    plt.show()

def print_tweet(t):
    print('User {0} tweeted: {1}'.format(t.screen_name, t.tweet_text))
    print('at {0}, with {1} retweets'.format(str(t.created_at), t.retweet_count))
    print('{0} has {1} followers, {2} friends, {3} verified'.format(t.screen_name, str(t.followers_count), str(t.friends_count),'is' if t.verified == 1 else 'is not'))
    print('p classification {0}, sentiment {1}'.format(pclassification(t), t.classification))


num_tweets = 0
pull_from_db = False
try:
    num_tweets = int(sys.argv[1])
    if sys.argv[2] == 'pull':
        pull_from_db = True
except:
    print('Usage: python analysis.py <num_tweets> <pull?>')
    exit()

list_tweets = []
fname = 'tweet_list.pickle'
sample_fname = 'sample_tweet_list.pickle'

if pull_from_db:
    start = time.time()
    list_tweets = get_all_tweets(100)
    end = time.time()
    elapsed = end - start
    print('Took {0} seconds to pull {1} tweets'.format(str(elapsed), len(list_tweets)))
    #pickle_tweets(list_tweets, fname)
else:
    list_tweets = unpickle_tweets(sample_fname)

# days = get_normalize_days(list_tweets, 10000)
# for k in days:
#     print ('Day: {0} has {1} tweets'.format(k, len(days[k])))
# import pickle
# pclasser = pickle.load(open('political_classification/c1.classifier', 'rb'))
# pol_leans = []
# for tweet in list_tweets[500:550]:
#     pol_lean = political_lean(pclasser.probs(tweet.tweet_text), tweet.polarity)
#     print(tweet.tweet_text)
#     print(pol_lean)

# days = in_days(list_tweets)
# plot_percent_positve_and_classifications(days)

#state_analysis(list_tweets)
# days = in_days(list_tweets)
# plot_togetherness(days)

# labeled_tweets = []
# labeled_tweets.extend(tweets_with_hashtag_to_labelled('obama', 1))
# labeled_tweets.extend(tweets_with_hashtag_to_labelled('obama2012', 1))
# labeled_tweets.extend(tweets_with_hashtag_to_labelled('obamabiden', 1))
# print('dem tweets', len(labeled_tweets))
# labeled_tweets.extend(tweets_with_hashtag_to_labelled('romney', 2))
# labeled_tweets.extend(tweets_with_hashtag_to_labelled('romney2012', 2))
# labeled_tweets.extend(tweets_with_hashtag_to_labelled('romneyryan', 2))
# print('full length', len(labeled_tweets))
# #
# with open('labelled.json', 'w') as f:
#     json.dump(labeled_tweets, f)
# obama_tweets = get_tweets_with_hashtag('obama', num_tweets)
# romney_tweets = get_tweets_with_hashtag('romneyryan', num_tweets)
# print(romney_tweets[10].tweet_text)
#
# print(percent_political_classifcation(obama_tweets))
# print(sentiments(obama_tweets))
# print(percent_political_classifcation(romney_tweets))
# print(sentiments(romney_tweets))
# (MAX_RTS, MAX_FOLLOWERS) = get_maxes(list_tweets)
#
# sort_by_weight = sorted(list_tweets, key=lambda t: weight(t))
# print_tweet(sort_by_weight[-4])
# print_tweet(sort_by_weight[-5])
# print_tweet(sort_by_weight[-6])


# states = in_states(list_tweets)
# pscores = {}
# (MAX_RTS, MAX_FOLLOWERS) = get_maxes(list_tweets)
#
# for k in states:
#     pscores[k] = political_score(states[k], MAX_RTS, MAX_FOLLOWERS)
#
#
# print([(k, pscores[k]) for k in sorted(pscores, key=pscores.get)])
# days = in_days(list_tweets)
# plot_percent_positive_per_day(days)
#state_analysis(list_tweets)

#in_states(list_tweets)
# locs = in_locations(list_tweets)
# for k in locs:
#     if len(locs[k]) > 5:
#         print ('Location: {0} has {1} tweets'.format(k, len(locs[k])))

#plot_percent_pclassification_per_day(days)
#plot_percent_pclassification_probs_per_day(days)

#plot_percent_positive_per_day(days)
