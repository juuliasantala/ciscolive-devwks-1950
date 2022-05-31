#!/usr/bin/env bash

startvpn.sh &

mkdir -p /home/developer/.ssh
echo "Host *
    KexAlgorithms +diffie-hellman-group14-sha1" > /home/developer/.ssh/config

echo "Installing requirements..."
pip install pyats[full] -q
echo "Done!\n"

echo "Verifying..."
echo "Connecting to Webex: "
curl -s -o /dev/null -w "%{http_code}" https://webexapis.com/v1/rooms/$WEBEX_ROOM -H "Accept: application/json" -H "Authorization: Bearer $WEBEX_TOKEN"

echo "\nConnecting to switch using RESTCONF: "
curl -s -o /dev/null -w "%{http_code}" -k https://$CSR_IP/restconf/ -u "$CSR_USERNAME:$CSR_PASSWORD"

echo "\nverifying pyATS:"
pyats version check

echo "\nSetup ready!"
