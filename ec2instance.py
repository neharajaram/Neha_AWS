# This file will create an EC2 instance
import boto3


ec2  = boto3. resource('ec2')


instances = ec2.create_instances(
	ImageId='ami-07f9ebd98e32b6dfd',
	MinCount=1,
	MaxCount=1,
	KeyName="WebServerkey",
	InstanceType="t2.micro"
	)
print('Instance Created')
	
for instance in instances:
	print (instance.id, instance.instance_type)
