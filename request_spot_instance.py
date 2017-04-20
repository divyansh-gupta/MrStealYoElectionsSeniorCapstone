import boto3

client = boto3.client('ec2', region_name='us-east-1', aws_access_key_id='***REMOVED***', aws_secret_access_key='***REMOVED***')

response = client.request_spot_fleet (
    DryRun = False,
    SpotFleetRequestConfig= {
    "IamFleetRole": "***REMOVED***",
    "AllocationStrategy": "lowestPrice",
    "TargetCapacity": 5,
    "SpotPrice": "0.025",
    "ValidFrom": "2017-04-19T15:21:10Z",
    "ValidUntil": "2018-04-19T15:21:10Z",
    "TerminateInstancesWithExpiration": True,
    "LaunchSpecifications": [
      {
        "ImageId": "ami-f4cc1de2",
        "InstanceType": "r4.large",
        "KeyName": "social-media",
        "EbsOptimized": True,
        "Monitoring": {
          "Enabled": True
        },
        "BlockDeviceMappings": [
          {
            "DeviceName": "/dev/sda1",
            "Ebs": {
              "DeleteOnTermination": True,
              "VolumeType": "gp2",
              "VolumeSize": 8,
              "SnapshotId": "***REMOVED***"
            }
          }
        ],
        "SecurityGroups": [
          {
            "GroupId": "***REMOVED***"
          }
        ],
        "UserData": "***REMOVED***"
      }
    ],
    "Type": "maintain",
    "ReplaceUnhealthyInstances": True
  }
)