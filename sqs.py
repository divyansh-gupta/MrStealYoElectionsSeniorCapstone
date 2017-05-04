import boto3
import uuid
import json

sqs = boto3.resource('sqs', region_name='us-east-1', aws_access_key_id='', aws_secret_access_key='')
def get_queue(name):
    return sqs.get_queue_by_name (
        QueueName=name
    )

def recieve_messages(queue_object, number, wait_time):
    return queue_object.receive_messages (
        MaxNumberOfMessages=number,
        WaitTimeSeconds=wait_time
    )

def lambda_handler(event, context):
    event_body = json.loads(event['body'])
    queue = get_queue(event_body['queue'])
    response = queue.send_message (
        MessageBody=str(event_body['message_body'])
    )
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(event_body)
    }