from rds import *
import tweepy

users = User.select()




non_english_users = []
for user in users:
