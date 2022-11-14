#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Webex sample function to send a message using a bot.

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

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

def post_message(message, token=os.getenv("WEBEX_TOKEN"), roomid=os.getenv("WEBEX_ROOM")):
    '''
    A function to send a text based message to a Webex room.
    '''
    print(f"Sending message: {message}")
    url = "https://webexapis.com/v1/messages"
    headers = {"authorization":f"Bearer {token}", "Content-Type":"application/json"}
    payload = {
        "roomId":roomid,
        "text":message
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status code of sending the Webex message: {response.status_code}")
    if str(response.status_code)[0] != "2":
        print("Error:")
        print(response.text)

if __name__ == "__main__":
    post_message("Hello Cisco Live :)")
