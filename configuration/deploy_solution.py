import requests
import urllib3
import jinja2
import yaml
import os

urllib3.disable_warnings()

def edit_interfaces(ip, username, password, config):
    url = f"https://{ip}:443/restconf/data/ietf-interfaces:interfaces"
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
    }
    auth = (username, password)

    response = requests.put(url, headers=headers, auth=auth, data=config, verify=False)
    print(f"Status code of deploying the configuration change: {response.status_code}")

def create_config(template, values):
    with open(values) as v:
        config = yaml.safe_load(v.read())
    with open(template) as t:
        template = jinja2.Template(t.read())
    
    configuration = template.render(interfaces=config["interfaces"])
    print(f"Configuration to be sent: \n {configuration}")
    return configuration

if __name__ == "__main__":

    # DEVICE DETAIL
    csr_ip = os.getenv("CSR_IP")
    csr_user = os.getenv("CSR_USERNAME")
    csr_password = os.getenv("CSR_PASSWORD")

    # CONFIGURATION
    interface_config = create_config("template.j2", "interfaces.yaml")
    edit_interfaces(csr_ip, csr_user, csr_password, interface_config)