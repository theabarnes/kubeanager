#!/home/opal/myenv/bin/python3
import os
import logging
import subprocess
import datetime
import codecs
import sys
import json
import logging
import boto3, botocore
from botocore.exceptions import ClientError

testvar=sys.argv[1]
test = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
testing2 = subprocess.Popen(["/bin/echo", "kops", "delete", "cluster", "--name", testvar, "--yes"], stdout=subprocess.PIPE).stdout.read().strip().decode("utf-8")

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

#print("testing", test)

print(test, "Deleting", testvar, testing2)


#def test_func():
#print(subprocess.Popen(["/bin/echo", "testing subprocess"], stdout=subprocess.PIPE).stdout.read().strip())
#    return True

#print(test_func())


#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#logging.warning('%s This will get logged to a file', test)
