#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sample code that makes an initial pre-test, configures devices, makes post-test
to verify that thetest passes after the change, and sends the test result to
Webex space.

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
import pathlib

from configuration.deploy_route_change import edit_routes, create_config
from change_verification.ping_test import make_ping_test
from notifications.webex_functions import post_message

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# SETUP: DEFINING GLOBAL VARIABLES:
DEVICE_IP = os.getenv("DEVICE_IP")
DEVICE_USER = os.getenv("DEVICE_USERNAME")
DEVICE_PASSWORD = os.getenv("DEVICE_PASSWORD")

ROUTE_TEMPLATE = (pathlib.Path(__file__).parent).joinpath('configuration', 'template.j2')
ROUTE_VALUES = (pathlib.Path(__file__).parent).joinpath('configuration', 'static_routes.yaml')

TESTBED = (pathlib.Path(__file__).parent).joinpath('change_verification', 'testbed.yaml')
PING_DESTINATIONS = ('208.67.222.222', '172.30.1.1')

# THE FLOW IS EXECUTED WHEN THIS main.py SCRIPT IS RUN:
if __name__ == "__main__":
    # 1. MAKE A TEST BEFORE APPLYING THE CHANGE
    pre_test = make_ping_test(TESTBED, PING_DESTINATIONS)

    # 2. MAKE CONFIG CHANGE
    configuration = create_config(ROUTE_TEMPLATE, ROUTE_VALUES)
    edit_routes(DEVICE_IP, DEVICE_USER, DEVICE_PASSWORD, configuration)

    # 3 MAKE A TEST AFTER APPLYING THE CHANGE
    post_test = make_ping_test(TESTBED, PING_DESTINATIONS)

    # 4. SEND TO WEBEX with a nice, clear message
    message = f"""
Ping test **before** configuration change: **{pre_test[0]}**
**Details:** {pre_test[1]}

Ping test **after** configuration change: **{post_test[0]}**
**Details:** {post_test[1]}
    """

    post_message(message)
