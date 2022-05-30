#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyATS sample functions for taking a snapshot of the network and comparing two
snapshots to find the differences..

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
from pyats import topology
from genie.utils.diff import Diff

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

def get_snapshot(testbed_file, uut, feature):
    '''
    Function that returns a snapshot of the selected feature.
    '''
    print(f"Connecting to {uut} for snapshot.")
    testbed = topology.loader.load(testbed_file) # load the testbed
    device = testbed.devices[uut] # find device with hostname / alias
    device.connect(log_stdout=False) # connect to the device
    snapshot = device.learn(feature) # learn a selected feature such as VLAN
    print("Snapshot ready")
    device.disconnect()
    return snapshot

def find_difference(snapshot1, snapshot2):
    '''
    Function to compare two snapshots and find the possible differences.
    '''
    print("finding differences")
    difference = Diff(snapshot1, snapshot2, exclude=["device", "accounting", "counters", "rate", "maker"]) # Define the snapshots to compare
    difference.findDiff() # Find differences between the snapshots defined
    return difference

if __name__ == '__main__':
    pre_snapshot = get_snapshot("testbed.yaml", "csr1000v-1", "all")
    post_snapshot = get_snapshot("testbed.yaml", "csr1000v-1", "all")
    diff = find_difference(pre_snapshot, post_snapshot)
    print(diff)

