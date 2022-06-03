import os

from configuration.deploy_solution import edit_interfaces, create_config
from change_verification.verify import get_snapshot, find_difference
from notifications.webex_functions import post_message

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