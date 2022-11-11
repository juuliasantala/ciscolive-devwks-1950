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

DESTINATIONS = ('208.67.222.222', '173.30.1.1')

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
        in the DESTINATIONS list. If the ping is successful, the test step is marked passed,
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

    @aetest.cleanup
    def disconnect(self, testbed):
        """
        Cleanup after the ping test by disconnecting from all testbed devices.
        """
        testbed.disconnect()

def make_ping_test(testbed_path):

    #if want to use a file
    import logging
    file_handler = logging.FileHandler(filename="pyats_output.log", mode="w+")
    logging.getLogger("pyats.aetest").addHandler(file_handler) 


    #If want to use a variable
    from io import StringIO as StringBuffer
    pyats_output_logger = StringBuffer()
    logging_handler = logging.StreamHandler(pyats_output_logger)
    logging.getLogger("pyats.aetest").addHandler(logging_handler)

    testbed = topology.loader.load(testbed_path)
    my_test = aetest.main(testbed=testbed)

    #these collect the info for variable
    log_contents = pyats_output_logger.getvalue()
    pyats_output_logger.close()
    print("logger variable:\n\n")
    print(log_contents) 

if __name__ == "__main__":
    testbed = "testbed.yaml"
    make_ping_test(testbed)


