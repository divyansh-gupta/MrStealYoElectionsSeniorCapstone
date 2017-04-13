import MySQLdb
import peewee
import datetime
from peewee import *
from playhouse.shortcuts import RetryOperationalError

import globals

############ EXAMPLE CODE ###############

# db = MySQLdb.connect(host="***REMOVED***",
#                      user="***REMOVED***",        
#                      passwd="***REMOVED***",
#                      db="socialnetworkingdb")

# you must create a Cursor object. It will let
#  you execute all the queries you need
# cur = db.cursor()

# Use all the SQL you like
# cur.execute("CREATE TABLE CUSTOMERS(ID INT NOT NULL, NAME VARCHAR (20) NOT NULL, PRIMARY KEY (ID));")

# print all the first cell of all the rows
# for row in cur.fetchall():
#     print row[0]

# db.close()

############ Pwiz & Peewee Models ###############

''' The following models were autoproduced using this command:
    python -m pwiz -e mysql \
	-H ***REMOVED*** \
	-u ***REMOVED*** socialnetworkingdb -P >> Models.py
'''

# class RetryDB(RetryOperationalError, MySQLDatabase):
    # pass

database = MySQLDatabase (
    'socialnetworkingdb', 
    threadlocals = True,
    use_speedups = True,
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

############ Real Code ###############

@database.atomic()
def bulk_insert_on_conflict_replace(Model, rows):
    try:
        query = peewee.InsertQuery(Model, rows=rows)
        query.upsert(upsert=True).execute()
    except Exception as e:
        print "Exception caught: ", str(e)
        bulk_insert_on_conflict_replace(Model, rows)

def disable_foreign_key_checks():
    database.execute_sql("SET FOREIGN_KEY_CHECKS = 0;")

def enable_foreign_key_checks():
    database.execute_sql("SET FOREIGN_KEY_CHECKS = 1;")

# lol = {'created_at': datetime.datetime(2012, 9, 9, 21, 17, 55), 
# 'retweet_count': 0, 'user': u'215440345', 
# 'tweet_text': u'Obama vies for health care edge in Florida - http://t.co/OcISvreb http://t.co/FsJ7xgGW #florida', 
# 'id': u'244907511377965056'}

# bulk_insert_on_conflict_replace(Tweet, [lol])

# select count(*) from HASHTAG; select count(*) from TWEET; select count(*) from TWEETPOLITICAL; select count(*) from TWEETSENTIMENT; select count(*) from USER;

# At 3:42 the program had been running for 4 minutes