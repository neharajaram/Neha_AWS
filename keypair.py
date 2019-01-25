# This program demonstrate creating a key pair that will be necessary to log in to the ec2 instance


import boto3

ec2  = boto3. resource('ec2')

#Create a keypair for the web server. The following lines of code will generate 
#Create a keypair and store it in a file in a directory
outfile = open ('WebServer.pem', 'w')
key_pair =  ec2.create_key_pair(KeyName='WebServerkey')
KeypairOut =str(key_pair.key_material)
outfile.write(KeypairOut)