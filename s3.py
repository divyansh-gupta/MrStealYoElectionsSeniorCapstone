import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print (bucket.name)

def push_to_s3 (bucket_name, file_key, body):
    # data = open('test.jpg', 'rb') is an example of how to how to open a file
    s3.Bucket(bucket_name).put_object(Key=file_key, Body=body)

# def get_from_s3 (arg):
#     pass
