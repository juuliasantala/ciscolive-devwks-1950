import os
import requests
import urllib3
import yaml
import jinja2

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

def create_config(template, values, device="csr1000v-1"):
    with open(values) as v:
        config = yaml.safe_load(v.read())
    with open(template) as t:
        template = jinja2.Template(t.read())
    
    configuration = template.render(device=config[device])
    print(f"Configuration to be sent: \n {configuration}")
    return configuration

def edit_config(device, target, config):
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/{target}"
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
    }
    auth = (device['user'], device['pw'])
    payload = config

    response = requests.put(url, headers=headers, auth=auth, data=payload, verify=False)
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

    configuration = create_config("template.j2", "configuration.yaml")

    edit_config(router, "interface", configuration)
    config_response = get_config(router)
    for loopback in config_response["Loopback"]:
        print(loopback)
