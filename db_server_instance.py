import os
import boto3
ec2 = boto3.resource('ec2')
outfile = open('SGDBServer.pem','w')
key_pair = ec2.create_key_pair(KeyName='SGDBServerKey')
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)
# 0o400 is used to set read permissions for the file as described in 
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
# Locate the private key and verify permissions

os.chmod('SGDBServer.pem', 0o400)

sg = ec2.create_security_group(
        GroupName="N-SG-DB",
        Description="Security group for DB Server")
		

# Define rule for all instances in the security group.
# since this is a db server, we allow access only from Web server
ip_ranges = [{  
    'CidrIp': '172.31.23.0/20'
}]

# Opens up port 80 (http), 443 (https) and 22 (ssh) on the instances
# associated with security groups.
permissions = [{  
    'IpProtocol': 'TCP',
    'FromPort': 22,
    'ToPort': 22,
    'IpRanges': ip_ranges,
}, {
    'IpProtocol': 'TCP',
    'FromPort': 3306,
    'ToPort': 3306,
    'IpRanges': ip_ranges,
}]


# Use these rules in the security group that got created
sg.authorize_ingress(IpPermissions=permissions)


# Spin up an instance and see it come alive in dashboard.
instances = ec2.create_instances(
    ImageId='ami-07f9ebd98e32b6dfd', 
    MinCount=1, 
    MaxCount=1,
    KeyName="SGDBServerKey",
    SecurityGroupIds=[sg.id],
    InstanceType="t2.micro"
)

instances[0].wait_until_running()


for instance in instances:
    print(instance.id, instance.instance_type, instance.public_dns_name)

