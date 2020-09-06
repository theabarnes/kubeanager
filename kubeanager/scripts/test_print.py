#!/home/opal/myenv/bin/python3
import os
import logging
import subprocess
import codecs
import sys
import json
import logging
import boto3, botocore
from botocore.exceptions import ClientError

testvar=sys.argv[1]

bucketname=sys.argv[2]

s3 = boto3.resource('s3')

def check_bucket(bucket):
    try:
        s3.meta.client.head_bucket(Bucket=bucketname)
        print("Bucket exist: s3://" + bucketname)
        return True
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access!")
            return True
        elif error_code == 404:
            print("Bucket Does Not Exist!")
            return False

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger()

f = codecs.open("deleted" + testvar + "deleted", "w+", encoding='utf8')
f.write("Cluster Deleted")
f.close()

print("Another Test")

print(check_bucket(bucketname))


#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#logging.warning('%s This will get logged to a file', test)
