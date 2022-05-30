import os

from configuration.deploy import edit_config, create_config, get_config
from change_verification.verify import get_snapshot, find_difference
from notifications.webex_functions import post_message

ROUTER = {
    "ip": os.getenv("CSR_IP"),
    "user": os.getenv("CSR_USERNAME"),
    "pw": os.getenv("CSR_PASSWORD"),
    "port": 443
}

if __name__ == "__main__":

    # 1. TAKE PRE-SNAPSHOT
    pre_snapshot = get_snapshot("./change_verification/testbed.yaml", "csr1000v-1", "interface")

    # 2. MAKE CONFIG CHANGE

    configuration = create_config("./configuration/template.j2", "./configuration/configuration.yaml")
    edit_config(ROUTER, "interface", configuration)

    # 3. TAKE POST-SNAPSHOT
    post_snapshot = get_snapshot("./change_verification/testbed.yaml", "csr1000v-1", "interface")

    # 4. FIND DIFF
    difference = find_difference(pre_snapshot, post_snapshot)

    # 5. SEND TO WEBEX
    message = f"Network configuration changed:\n{difference}"
    post_message(message)