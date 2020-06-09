#!/home/opal/myenv/bin/python3
import os
import subprocess
import sys
import codecs
import json
import logging
import boto3, botocore
import time
from botocore.exceptions import ClientError

bucketname=sys.argv[1]
clustername=sys.argv[2]
dnszone=sys.argv[3]
profile=sys.argv[4]

s3 = boto3.resource('s3')
session = boto3.session.Session(profile_name=profile)
iam = session.client('iam')
client = boto3.client('iam')
bucket = s3.Bucket(bucketname)
account_id = boto3.client('sts').get_caller_identity().get('Account')
KOPS_STATE_STORE=os.environ['KOPS_STATE_STORE'] = 's3://' + bucketname
role_name='KubernetesAdmin'

def check_role(role):
   try:
       # Create IAM Role and Policy

       response = client.get_role(
           RoleName=role_name
       )
       print("Skip ")
       return False
   except client.exceptions.NoSuchEntityException as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            print("Create ")
            return True

def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            createdBucket = s3_client.create_bucket(Bucket=bucket_name)
            print(createdBucket)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def create_role(role):
    # Create IAM Role and Policy
    path='/'
    #role_name='KubernetesAdmin'
    description='Kubernetes administrator role (for AWS IAM Authenticator for Kubernetes).'

    trust_policy={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Condition": {},
                "Principal": {
                    "AWS": "arn:aws:iam::" + account_id + ":root"
                }
            }
        ]
    }

    response = iam.create_role(
        Path=path,
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description=description,
        MaxSessionDuration=3600
    )

    policy_output=json.dumps(trust_policy)
    print(policy_output + ' ')

subprocess.Popen(["/bin/mkdir", "-p", "kubeanager/clusters/" + clustername])

checkrole=check_role(role_name)

if checkrole:
    print("Creating role ")
    create_role(role_name)
else:
    print("Skip creation ")

create_bucket(bucketname)


#createCluster=subprocess.Popen(["/usr/local/bin/kops", "create", "cluster", "--name", clustername, "--zones", "us-east-1a", "--state", KOPS_STATE_STORE, "--node-size", "m3.large", "--master-size", "m3.medium", "--node-count", "3", "--master-count", "3", "--dns-zone", dnszone, "--topology", "private", "--networking", "calico"], stdout=subprocess.PIPE)
#CREATECLUSTER=createCluster.stdout.read().strip()
#print(CREATECLUSTER)

#updateCluster=subprocess.Popen(["/usr/local/bin/kops", "update", "cluster", "--name", clustername, "--yes"], stdout=subprocess.PIPE)
#UPDATECLUSTER=updateCluster.stdout.read().strip()

f = codecs.open("kubeanager/clusters/" + clustername + "/completed", "w+", encoding='utf8')
f.write("Cluster Created")
f.close()

print("Cluster Created")
#time.sleep(300.9)

#validateCluster=subprocess.Popen(["/usr/local/bin/kops", "kops validate cluster"], stout=ssubprocess.PIPE)
#VALIDATECLUSTER=validateCluster.stdout.read().strip()
#print(VALIDATECLUSTER_=)
