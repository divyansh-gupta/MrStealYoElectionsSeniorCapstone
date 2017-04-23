import requests
import json

api_gateway_key = '***REMOVED***'

def queue_task(url, queue, message_body):
	r = requests.post(url, data = json.dumps({ 'queue': queue, 'message_body': message_body }),
		headers = {'x-api-key': api_gateway_key })
	print(r.status_code, r.reason, r.text)

def queue_2012_tasks(start_inclusive, end_exclusive):
	for i in range(start_inclusive, end_exclusive):
		queue_task("***REMOVED***", "2012", i)

queue_2012_tasks(0, 1)
