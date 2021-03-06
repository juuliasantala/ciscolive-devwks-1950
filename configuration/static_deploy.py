import requests
import urllib3

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
