#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for changing interface configuration with RESTCONF.

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
import requests
import urllib3

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

urllib3.disable_warnings()

def get_interfaces(ip, username, password):
    '''Get interfaces using RESTCONF'''

    url = f"https://{ip}:443/restconf/data/ietf-interfaces:interfaces"
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
    }
    auth = (username, password)

    response = requests.get(url, headers=headers, auth=auth, verify=False)
    print(f"Printing out the interfaces on device {ip}:\n")
    for interface in response.json()["ietf-interfaces:interfaces"]["interface"]:
        print(f"- {interface['name']}(Enabled: {interface['enabled']})")
        print(f"  {interface['description']}")
        if "address" in interface["ietf-ip:ipv4"]:
            print(f"  IP address: {interface['ietf-ip:ipv4']['address'][0]['ip']}")

if __name__ == "__main__":

    # DEVICE DETAIL
    CSR_IP = os.getenv("CSR_IP")
    CSR_USER = os.getenv("CSR_USERNAME")
    CSR_PASSWORD = os.getenv("CSR_PASSWORD")

    get_interfaces(CSR_IP, CSR_USER, CSR_PASSWORD)
