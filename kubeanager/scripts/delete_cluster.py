#!/home/opal/myenv/bin/python3
import os
import subprocess
import sys
import logging
import boto3, botocore
from botocore.exceptions import ClientError

clustername=sys.argv[1]
bucketname=sys.argv[2]
profile=sys.argv[3]

s3 = boto3.resource('s3')
session = boto3.session.Session(profile_name=profile)
iam = session.client('iam')
client = boto3.client('iam')
bucket = s3.Bucket(bucketname)
account_id = boto3.client('sts').get_caller_identity().get('Account')
KOPS_STATE_STORE=os.environ['KOPS_STATE_STORE'] = 's3://' + bucketname
role_name='KubernetesAdmin'

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("kubeanager/clusters/" + clustername + "/deleted.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger()

def delete_cluster():
    #subprocess.Popen(["/usr/local/bin/kops", "delete", "cluster", "--name", clustername, "--yes"], stdout=subprocess.PIPE).stdout.read().strip()
    subprocess.Popen(["/bin/echo", "kops", "delete", "cluster", "--name", clustername, "--yes"], stdout=subprocess.PIPE).stdout.read().strip()
    return True

print(delete_cluster())
