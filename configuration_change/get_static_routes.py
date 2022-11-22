#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
# from pprint import pprint
import requests
import urllib3

urllib3.disable_warnings()

def get_routes(ip, username, password):
    '''Get interfaces using RESTCONF'''

    url = f"https://{ip}:443/restconf/data/Cisco-IOS-XE-native:native/ip/route"
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
    }
    auth = (username, password)

    response = requests.get(url, headers=headers, auth=auth, verify=False)
    print(f"\nThe response body for static routes on device {ip}:\n")
    # pprint(response.json()) 
    response = response.json()
    formatted = json.dumps(response, indent=2)
    print(formatted)

if __name__ == "__main__":

    # DEVICE DETAIL
    DEVICE_IP = os.getenv("DEVICE_IP")
    DEVICE_USER = os.getenv("DEVICE_USERNAME")
    DEVICE_PASSWORD = os.getenv("DEVICE_PASSWORD")

    get_routes(DEVICE_IP, DEVICE_USER, DEVICE_PASSWORD)
