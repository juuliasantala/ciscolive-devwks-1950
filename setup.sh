#!/bin/bash

. ./env

echo "GET READY FOR YOUR CISCO LIVE WORKSHOP EXPERIENCE :)"
echo -n "What is your pod number? "
read POD_NUMBER

POD_NUMBER=$(echo ${POD_NUMBER} | sed 's/^0*//')

export POD_NUMBER=$(printf "%02d" "${POD_NUMBER}")
export DEVICE_IP="64.102.247.2${POD_NUMBER}"

python ./setup_test.py
