import boto3

s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print (bucket.name)

def push_to_s3 (bucket_name, file_key, body):
    # data = open('test.jpg', 'rb') is an example of how to how to open a file
    picked_bucket = s3.Bucket(bucket_name)
    picked_bucket.put_object(Key=file_key, Body=body)

def download_from_s3 (bucket_name, file_key, location_save_to, open_and_return_file_bool):
    s3.meta.client.download_file(bucket_name, file_key, location_save_to)
    if open_and_return_file_bool:
    	# make sure to close the file later, if you open it!
    	return open(location_save_to, 'r')
