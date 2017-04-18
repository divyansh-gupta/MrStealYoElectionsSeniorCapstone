import boto3

sqs = boto3.resource('sqs', region_name='us-east-2')

def get_queue(name):
	return sqs.get_queue_by_name (
    	QueueName=name
   	)

def recieve_messages(queue_object, number, wait_time):
	return queue_object.receive_messages(
		MaxNumberOfMessages=number,
		WaitTimeSeconds=wait_time
	)