'''
Simple example of a Ping testcase using pyATS.

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
'''

from pyats import aetest, topology

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

DESTINATIONS = ('8.8.8.8', '173.30.1.1')

class PingTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking connectivity from the network devices.
    '''
    @aetest.setup
    def connect(self, testbed):
        '''
        Setup task: connect to all devices in the testbed and define that the
        test function "ping" should be repeated for each device in the testbed.
        '''
        testbed.connect(log_stdout=False)
        aetest.loop.mark(self.ping, device=testbed)


    @aetest.test
    def ping(self, steps, device):
        '''
        Simple ping test: using pyats API "ping", try pinging each of the IP addresses
        in the DESTINATION list. If the ping is successful, the test step is marked passed,
        but if the ping is unsuccesful, the step is marked as failed.
        '''
        for destination in DESTINATIONS:
            with steps.start(
                f"Checking Ping from {device.hostname} to {destination}", continue_=True
                ) as step:
                try:
                    device.ping(destination)
                except:
                    step.failed(f'Ping {destination} from device {device.hostname} unsuccessful')
                else:
                    step.passed(f"Ping {destination} from device {device.hostname} successful")
            # print(steps.details)
            # steps.report()

    @aetest.cleanup
    def disconnect(self, testbed):
        """
        Cleanup after the ping test by disconnecting from all testbed devices.
        """
        testbed.disconnect()

def main():
    testbed = "testbed.yaml"
    testbed = topology.loader.load(testbed)
    my_test = aetest.main(testbed=testbed)

if __name__ == "__main__":
    main()

