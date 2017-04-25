import pyximport; pyximport.install()
import os
import json

from cmain import api
from fix_db_inconsistencies import *
from api_gateway import *
import sqs

if os.path.exists('2012_data') is False:
    os.makedirs('2012_data')
if os.path.exists('2016_data') is False:
    os.makedirs('2016_data')

queue_2012 = sqs.get_queue('2012')
queue_2012_finished = sqs.get_queue('2012_finished')

def top_level_get_and_process_tweets(x, process_all):
    api.get_and_process_tweets(x, process_all)

def long_poll_2012():
    messages = []
    while len(messages) == 0:
        messages = sqs.recieve_messages(queue_2012, 1, 20)
    messages[0].delete()
    print(messages[0].body)
    message_body = json.loads(messages[0].body)
    x = message_body['file_number']
    process_all = message_body['process_all'].lower() == 'true'
    try:
        top_level_get_and_process_tweets(x, process_all)
    except Exception as e:
        queue_2012_task(x, process_all)
        print(e)
    else:
        notify_2012_task_finished(message_body)
    reclassify_sentiment()
    reclassify_politics()

while True:
    long_poll_2012()
