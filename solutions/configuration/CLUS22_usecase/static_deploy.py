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

import requests
import urllib3

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

urllib3.disable_warnings()

def edit_interfaces(ip, username, password, config):
    '''Edit interfaces based on a configuration file.'''

    url = f"https://{ip}:443/restconf/data/ietf-interfaces:interfaces"
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
    }
    auth = (username, password)

    response = requests.put(url, headers=headers, auth=auth, data=config, verify=False)
    print(f"Status code of deploying the configuration change: {response.status_code}")

if __name__ == "__main__":

    # DEVICE DETAIL
    CSR_IP = "10.10.20.48"
    CSR_USER = "developer"
    CSR_PASSWORD = "C1sco12345"

    # CONFIGURATION
    interface_config = '''
    {
        "ietf-interfaces:interfaces": {
            "interface": [
                {
                    "name": "GigabitEthernet1",
                    "description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": true,
                    "ietf-ip:ipv4": {
                        "address": [
                            {
                                "ip": "10.10.20.48",
                                "netmask": "255.255.255.0"
                            }
                        ]
                    }
                },
                {
                    "name": "GigabitEthernet2",
                    "description": "Network Interface",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": false
                },
                {
                    "name": "GigabitEthernet3",
                    "description": "Network Interface",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": false
                },
                {
                    "name": "Loopback1",
                    "description": "Configured from Python",
                    "type": "iana-if-type:softwareLoopback",
                    "enabled": true,
                    "ietf-ip:ipv4": {
                        "address": [
                            {
                                "ip": "10.20.50.20",
                                "netmask": "255.255.255.0"
                            }
                        ]
                    }
                }
            ]
        }
    }'''

    edit_interfaces(CSR_IP, CSR_USER, CSR_PASSWORD, interface_config)
