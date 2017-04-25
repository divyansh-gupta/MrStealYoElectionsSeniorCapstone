from flask import Flask
from flask import request
import flask 
import tweepy
app = Flask(__name__)

CALLBACK_URL = 'http://localhost:5000/verify'
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
    # db['access_token_key']=auth.access_token
    # db['access_token_secret']=auth.access_token.secret
    return flask.redirect(flask.url_for('start'))

@app.route("/start")
def start():
    #auth done, app logic can begin
    api = db['api']

    #example, print your latest status posts
    return flask.render_template('tweets.html', tweets=api.user_timeline())

if __name__ == "__main__":
    app.run()
