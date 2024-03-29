#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for retrieving infomration on the static route
configuration with RESTCONF.

Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import os
from pprint import pprint
import requests
import urllib3

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

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
    pprint(response.json())


if __name__ == "__main__":

    # DEVICE DETAIL
    DEVICE_IP = os.getenv("DEVICE_IP")
    DEVICE_USER = os.getenv("DEVICE_USERNAME")
    DEVICE_PASSWORD = os.getenv("DEVICE_PASSWORD")

    get_routes(DEVICE_IP, DEVICE_USER, DEVICE_PASSWORD)
