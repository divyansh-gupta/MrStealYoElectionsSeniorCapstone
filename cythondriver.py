import pyximport; pyximport.install()
import os

from cmain import TwitterClient
import sqs

def top_level_get_and_process_tweets(x):
    api = TwitterClient()
    api.get_and_process_tweets(x)

if os.path.exists('2012_data') is False:
    os.makedirs('2012_data')
if os.path.exists('2016_data') is False:
    os.makedirs('2016_data')

queue_2012 = sqs.get_queue('2012.fifo')

def long_poll_2012():
	messages = []
	while len(messages) == 0:
		messages = sqs.recieve_messages(queue_2012, 1, 20)
	print(messages)
	messages[0].delete()
	top_level_get_and_process_tweets(messages[0].body)

while True:
	long_poll_2012()