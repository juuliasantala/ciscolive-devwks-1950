import os
import requests
import urllib3

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
