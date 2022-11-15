import os
import requests
import urllib3
import jinja2
import yaml

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
    # Your code here!