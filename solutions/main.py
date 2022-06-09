#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sample code that takes snapshot, configures devices, takes a second snapshot
and sends the Diff of these snapshots to Webex space.

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

from configuration.dynamic_deploy import edit_interfaces, create_config
from change_verification.verify import get_snapshot, find_difference
from notifications.webex_functions import post_message

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

CSR_IP = os.getenv("CSR_IP")
CSR_USER = os.getenv("CSR_USERNAME")
CSR_PASSWORD = os.getenv("CSR_PASSWORD")

TESTBED = "./change_verification/testbed.yaml"
INTERFACE_TEMPLATE = "./configuration/template.j2"
INTERFACE_VALUES = "./configuration/interfaces.yaml"

if __name__ == "__main__":

    # 1. TAKE PRE-SNAPSHOT
    pre_snapshot = get_snapshot(TESTBED, "csr1000v-1", "interface")

    # 2. MAKE CONFIG CHANGE

    configuration = create_config(INTERFACE_TEMPLATE, INTERFACE_VALUES)
    edit_interfaces(CSR_IP, CSR_USER, CSR_PASSWORD, configuration)

    # 3. TAKE POST-SNAPSHOT
    post_snapshot = get_snapshot(TESTBED, "csr1000v-1", "interface")

    # 4. FIND DIFF
    difference = find_difference(pre_snapshot, post_snapshot)

    # 5. SEND TO WEBEX
    message = f"Network configuration changed:\n{difference}"
    post_message(message)
