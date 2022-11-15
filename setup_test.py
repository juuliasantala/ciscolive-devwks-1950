#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup function for DevNet workshop to be used in Cisco Live events.
"""

import os
import textwrap
import requests

# POD_IP = "64.102.247.2{pod}"

def setup_test():
    '''
    Setup testing for the workshop to verify the ENV variables are correctly in place.
    '''
    pod_number = os.getenv("POD_NUMBER")
    device_ip = os.getenv("DEVICE_IP")
    webex_room = os.getenv('WEBEX_ROOM')
    webex_token = os.getenv('WEBEX_TOKEN')

    errors = []
    wrapper = textwrap.TextWrapper(
                                initial_indent=' '*8,
                                width=80,
                                subsequent_indent=' '*8
                                )

    print(f"\n{'*'*40}\n")
    print("Executing connecivity tests to verify the setup was completed successfully.\n")

    print(f"TEST 1. Checking the connectivity to the router of pod {pod_number}:")
    response = os.popen(f"ping {device_ip} -c 3").read()
    for line in response.split("\n"):
        print(wrapper.fill(line))
    if "100.0% packet loss" in response:
        errors.append(
            f"Error in pinging pod {pod_number} ({device_ip}), 100% packet loss"
            )

    print("\nTEST 2. Checking connectivity to Webex space:")

    url = f"https://webexapis.com/v1/rooms/{webex_room}"
    headers = {
        "authorization":f"Bearer {webex_token}",
        "Content-Type":"application/json"
    }
    response = requests.get(url, headers=headers, timeout=60)
    if str(response.status_code)[0] == "2":
        print(wrapper.fill("SUCCESS!"))
    else:
        print(wrapper.fill("ERROR in reaching Webex space:"))
        print(wrapper.fill(response.text))
        errors.append(
            f"Error in reaching Webex space:\n{response.json()['message']}"
            )

    print(f"\n{'*'*40}\n")
    if errors:
        error_wrapper = textwrap.TextWrapper(
                                initial_indent=f"{' '*6}- ",
                                width=80,
                                subsequent_indent=' '*8
                                )
        print("THERE WERE ERRORS IN SETUP TESTING:")
        for error in errors:
            print(error_wrapper.fill(error))
        print("\n")
        print(wrapper.fill("Please ask proctor to help you!"))
    else:
        print("All checks done and everything seems to be working fine!")
        print("Have fun with the workshop!")

if __name__ == "__main__":
    setup_test()
