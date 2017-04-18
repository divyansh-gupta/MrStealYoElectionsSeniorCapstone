#!/bin/bash
cd /home/***REMOVED***
git clone "https://divyansh-gupta:***REMOVED***@github.com/zakkl13/sa_capstone_elections_project.git";
sudo apt-get -y update;
sudo apt-get install -y python3-pip;
sudo apt-get install -y python-mysqldb libmysqlclient-dev;
sudo pip3 install peewee pytz textblob tweepy boto3 Cython mysqlclient requests;
mkdir ~/.aws;
touch ~/.aws/config;
touch ~/.aws/credentials;
sudo chmod 777 ~/.aws/*;
sudo printf "[default]\naws_access_key_id = ***REMOVED***\naws_secret_access_key = ***REMOVED***" > ~/.aws/credentials
sudo printf "[default]\nregion=us-east-1" > ~/.aws/config;
cd /home/***REMOVED***/sa_capstone_elections_project;
python3 2012_consumer.py;
