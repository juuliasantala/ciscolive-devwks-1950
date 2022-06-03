#!/usr/bin/env bash

echo "Connecting to VPN..."
startvpn.sh &
echo "Connected!"

mkdir -p /home/developer/.ssh
echo "Host *
    KexAlgorithms +diffie-hellman-group14-sha1" > /home/developer/.ssh/config

echo " "
echo "Verifying..."
echo "Connecting to Webex: "
curl -s -o /dev/null -w "%{http_code}" https://webexapis.com/v1/rooms/$WEBEX_ROOM -H "Accept: application/json" -H "Authorization: Bearer $WEBEX_TOKEN"

echo " "
echo "Connecting to CSR using RESTCONF: "
curl -s -o /dev/null -w "%{http_code}" -k https://$CSR_IP/restconf/ -u "$CSR_USERNAME:$CSR_PASSWORD"

echo " "
echo "Connecting to CSR using pyATS to retrieve the platform details: "
pyats parse "show platform" --testbed-file ~/src/ciscolive-devwks-1950/solutions/change_verification/testbed.yaml

echo " "
echo "Setup ready!"
