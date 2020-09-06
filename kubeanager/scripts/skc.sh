#!/bin/bash

bucketname=$1
clustername=$2

kops get cluster --state s3://$bucketname

kubectl config set-context $(kubectl config get-contexts | grep $clustername | awk '{print $2}')
kubectl config use-context $(kubectl config get-contexts | grep $clustername | awk '{print $2}')
