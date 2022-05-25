import os
import requests
import urllib3

urllib3.disable_warnings()

def get_config(device):
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface"
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
    }
    auth = (device['user'], device['pw'])

    response = requests.get(url, headers=headers, auth=auth, verify=False)
    print(f"Status code of retrieving config: {response.status_code}")
    return response.json()["Cisco-IOS-XE-native:interface"]

def edit_config(device, target, config):
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/{target}"
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
    }
    auth = (device['user'], device['pw'])
    payload = config

    response = requests.post(url, headers=headers, auth=auth, json=payload, verify=False)
    print(f"Status code of deploying the configuration change: {response.status_code}")

if __name__ == "__main__":
    router = {
        "ip": os.getenv("CSR_IP"),
        "user": os.getenv("CSR_USERNAME"),
        "pw": os.getenv("CSR_PASSWORD"),
        "port": 443

    }
    if None in router.values():
        raise Exception("Check your env values!")

    config_response = get_config(router)
    for loopback in config_response["Loopback"]:
        print(loopback)

    config = {
        "Loopback": [
            {
                "name": "30",
                "description": "Postman",
                "ip": {
                    "address": {
                        "primary": {
                            "address": "10.60.20.48",
                            "mask": "255.255.255.0"
                        }
                    }
                }
            }
        ]
    }

    edit_config(router, "interface", config)
    config_response = get_config(router)
    for loopback in config_response["Loopback"]:
        print(loopback)
