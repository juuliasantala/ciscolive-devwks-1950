# Saturday Night and the Network's alright 

Solution files for Cisco Live 2022 DevNet workshop

## Requirements

- Target network device:
    - reservable CSR sandbox from [DevNet sandboxes](https://devnetsandbox.cisco.com/)
    - Validate that the current interface configuration on the reservable sandbox matches to what has been defined in the `configuration/interfaces.yaml` (apart from the Loopback). Make necessary changes in case the sandbox device has changed.
- Webex:
    - Webex Bot ([instructions on how to create one can be read here](https://developer.webex.com/docs/bots))
    - Webex room into which the Bot has been added
- Workstation from where the code is run:
    - Python 3.7 or newer installed
    - For `Hack 2: Change verification` Linux or Mac is required, as pyATS is not supported on Windows.

## Preparations

1. Copy / rename the `env.template` into `env`
```bash
$ mv env.template env
```

2. In the `env` file, fill in the IP address, username and password for the device you want to target. Note that it is expected that SSH and RESTCONF are enabled for the device, and that the credentials allow access to both of these.

```bash
# ROUTER settings
export CSR_IP=<FILL>
export CSR_USERNAME=<FILL>
export CSR_PASSWORD=<FILL>
```

3. In the `env` file, fill in the Webext token for the Webex bot (you get the token when you create the bot) and an ID of your Webex room. Your bot has to be added into the room for the code to work, as the bot needs to have rights to send a message in there. You can get the room ID with an API call ([see documentation here](https://developer.webex.com/docs/api/v1/rooms/list-rooms), easiest to find the correct room is to write a message there and then use the `sortBy=lastActivity` query parameter).

```bash
# Webex settings
export WEBEX_TOKEN=<FILL>
export WEBEX_ROOM=<FILL>
```

4. Back in your terminal, take the environment variables into use with `.` or `source`

```bash
$ . ./env
```

5. Create and activate a new virtual environment, and install the requirements from file `requirements.txt` in that venv.
```bash
$ python3 -m venv venv
$ source venv/bin/activate #when using mac/linux
$ pip install -r requirements.txt
```

## Authors & Maintainers
* Juulia Santala jusantal@cisco.com

## License
This project is licensed to you under the terms of the [Cisco Sample Code License](LICENSE).