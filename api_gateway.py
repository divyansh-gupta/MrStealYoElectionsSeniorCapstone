import requests
import json

api_gateway_key = ''
enqueue_endpoint = ""

def enqueue(url, queue, message_body):
    r = requests.post(url, 
        data = json.dumps({
            'queue': queue,
            'message_body': message_body
        }),
        headers = {'x-api-key': api_gateway_key }
    )
    print(r.status_code, r.reason, r.text)

# set process_all to true if you want to process every tweet in file
# instead of every 50th.
def queue_2012_task(file_number_or_str, process_all):
    enqueue(
        enqueue_endpoint, '2012',
        json.dumps({
            'file_number': str(file_number_or_str),
            'process_all': str(process_all)
        })
    )

def notify_2012_task_finished(message_body):
    enqueue(
        enqueue_endpoint, '2012_finished',
        json.dumps(message_body)
    )

# queue_2012_task(0, False)
