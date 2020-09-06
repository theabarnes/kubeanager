#!/home/opal/myenv/bin/python3
import os
import subprocess
import sys, traceback
import json
import logging
import boto3, botocore
from botocore.exceptions import ClientError
import botocore.exceptions

client = boto3.client('iam')

role_name='KubernetesAdmin'

def check_role(role):
   try:
       # Create IAM Role and Policy

       response = client.get_role(
           RoleName=role_name
       )
       print("Proceed")
       return True
   except client.exceptions.NoSuchEntityException as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            print("Create")
            return True

check_role(role_name)
