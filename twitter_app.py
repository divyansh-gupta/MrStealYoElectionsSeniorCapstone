from flask import Flask
from flask import request, Response
from flask_socketio import SocketIO, send, emit
import flask 
import tweepy
import json
import _thread as thread
from peewee import RawQuery
from datetime import datetime
import time

from rds import *
from s3 import *
from api_gateway import *

app = Flask(__name__)
socketio = SocketIO(app)

CALLBACK_URL = 'http://localhost:80/verify'
session = dict()
db = dict() # you can save these values to a database

@app.route("/")
def send_token():
    auth = tweepy.OAuthHandler('***REMOVED***', '***REMOVED***', CALLBACK_URL)
    try:
        redirect_url= auth.get_authorization_url()
        session['request_token'] = auth.request_token
    except tweepy.TweepError:
        print ('Error! Failed to get request token')
    
    return flask.redirect(redirect_url)

@app.route("/verify")
def get_verification():
    #get the verifier key from the request url
    verifier= request.args['oauth_verifier']
    
    auth = tweepy.OAuthHandler('***REMOVED***', '***REMOVED***')
    token = session['request_token']
    del session['request_token']
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print ('Error! Failed to get access token.')
    
    #now you have access!
    api = tweepy.API(auth)

    #store in a db
    db['api']= api
    return flask.redirect(flask.url_for('start'))

@app.route("/logout")
def logout():
    del db['api']
    return flask.redirect(flask.url_for('start'))

def get_results():
    try:
        api = db['api']
    except Exception as e:
        return flask.redirect('/')
    api = db['api']
    id_list = db[api.me().id_str]
    all_ids = ""
    for id_str in id_list:
        all_ids += id_str + ","
    tweets_found_ids = {}
    while True:
        print("querying")
        tweets_found = RawQuery(Tweet, "SELECT TWEET.*, TWEETPOLITICAL.classification from TWEET, TWEETPOLITICAL WHERE TWEET.ID IN (" + all_ids[:-1] + ") AND TWEETPOLITICAL.tweet_id = TWEET.ID ORDER BY TWEET.created_at")
        for tweet in tweets_found.dicts().execute():
            if tweet['id'] not in tweets_found_ids:
                tweets_found_ids[tweet['id']] = tweet['id']
                tweet['created_at'] = tweet['created_at'].isoformat()
                socketio.emit("recieve_tweet", json.dumps(tweet))
        if len(tweets_found_ids) == 500:
            return
        time.sleep(2)

def get_and_process_tweets(api):
    id_list = []
    s3_file_data = ""
    s3_file_key = '2012_data/cache-' + api.me().id_str + '.json'
    for status in tweepy.Cursor(api.user_timeline).items(500):
        status_json = status._json
        id_list.append(status_json['id_str'])
        s3_file_data += json.dumps(status._json) + "\n"
    print(len(id_list))
    db[api.me().id_str] = id_list
    push_to_s3('social-networking-capstone', s3_file_key, s3_file_data)
    queue_2012_task(api.me().id_str, True)
    thread.start_new_thread(get_results, ())

@app.route("/get_tweets")
def get_tweets():
    try:
        api = db['api']
    except Exception as e:
        return flask.redirect('/')
    api = db['api']
    get_and_process_tweets(api)
    return Response("200")

@app.route("/start")
def start():
    #auth done, app logic can begin
    try:
        api = db['api']
    except Exception as e:
        return flask.redirect('/')
    api = db['api']

    # example, print your latest status posts
    return flask.render_template('tweets.html')

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=80)
