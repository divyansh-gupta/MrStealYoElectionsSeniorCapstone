#!/bin/bash
cd /home/***REMOVED***
git clone "https://divyansh-gupta:<password>(@github.com/zakkl13/sa_capstone_elections_project.git";
sudo apt-get -y update;
sudo apt-get install -y python3-pip;
sudo apt-get install -y python-mysqldb libmysqlclient-dev python-virtualenv;
sudo pip3 install peewee pytz textblob tweepy boto3 Cython mysqlclient requests numpy scipy scikit-learn nltk flask zappa flask_socketio;
mkdir ~/.aws;
sudo touch ~/.aws/config;
sudo touch ~/.aws/credentials;
sudo chmod 777 ~/.aws/*;
sudo printf "[default]\naws_access_key_id = <aws_access_key_id>\naws_secret_access_key = <aws_secret_access_key>" > ~/.aws/credentials
sudo printf "[default]\nregion=us-east-1" > ~/.aws/config;
cd /home/***REMOVED***/sa_capstone_elections_project;
chmod 777 /home/***REMOVED***/sa_capstone_elections_project/*;
screen -d -m -L sudo python3 2012_consumer.py;
sudo touch banana.txt
