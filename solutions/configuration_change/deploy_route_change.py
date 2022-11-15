#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for changing static route configuration with RESTCONF.

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
import jinja2
import yaml

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

urllib3.disable_warnings()

def edit_routes(ip, username, password, config):
    '''Edit routing configuration based on a configuration file.'''

    url = f"https://{ip}:443/restconf/data/Cisco-IOS-XE-native:native/ip/route"
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
    }
    auth = (username, password)

    response = requests.put(url, headers=headers, auth=auth, data=config, verify=False)
    print(f"Status code of deploying the configuration change: {response.status_code}")
    if str(response.status_code)[0] != "2":
        print("Error:")
        print(response.text)

def create_config(template, values):
    '''Create a configuration from Jinja2 template and values from YAML file.'''

    with open(values, encoding="utf-8") as my_values:
        config = yaml.safe_load(my_values.read())
    with open(template, encoding="utf-8") as my_template:
        template = jinja2.Template(my_template.read())

    configuration = template.render(routes=config["routes"])
    print(f"Configuration to be sent: \n {configuration}")
    return configuration

if __name__ == "__main__":

    # DEVICE DETAIL
    DEVICE_IP = os.getenv("DEVICE_IP")
    DEVICE_USER = os.getenv("DEVICE_USERNAME")
    DEVICE_PASSWORD = os.getenv("DEVICE_PASSWORD")

    # CONFIGURATION
    interface_config = create_config("template.j2", "static_routes.yaml")
    edit_routes(DEVICE_IP, DEVICE_USER, DEVICE_PASSWORD, interface_config)
