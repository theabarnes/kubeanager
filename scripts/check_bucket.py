#!/home/opal/myenv/bin/python3
import os
import subprocess
import sys, traceback
import json
import logging
import boto3, botocore
from botocore.exceptions import ClientError

bucketname=sys.argv[1]

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

check_bucket(bucketname)
