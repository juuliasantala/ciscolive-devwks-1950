import requests
import urllib3

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

if __name__ == "__main__":

    # DEVICE DETAIL
    csr_ip = "10.10.20.48"
    csr_user = "developer"
    csr_password = "C1sco12345"

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
                    "name": "Loopback50",
                    "description": "Python",
                    "type": "iana-if-type:softwareLoopback",
                    "enabled": true,
                    "ietf-ip:ipv4": {
                        "address": [
                            {
                                "ip": "10.50.20.12",
                                "netmask": "255.255.255.0"
                            }
                        ]
                    }
                }
            ]
        }
    }'''

    edit_interfaces(csr_ip, csr_user, csr_password, interface_config)