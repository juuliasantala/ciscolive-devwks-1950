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
    def ping(self, steps, device, destinations, test_results):
        '''
        Simple ping test: using pyats API "ping", try pinging each of the IP addresses
        in the destinations tuple. If the ping is successful, the test step is marked passed,
        but if the ping is unsuccesful, the step is marked as failed.
        test_results dictionary is used to collect a summary of the results to be further used
        in for example sending the end result to Webex space.
        '''
        test_results[device.hostname] = {"Passed":[], "Failed":[]}
        for destination in destinations:
            with steps.start(
                f"Checking Ping from {device.hostname} to {destination}", continue_=True
                ) as step:
                try:
                    device.ping(destination)
                except:
                    test_results[device.hostname]["Failed"].append(destination)
                    step.failed(f'Ping {destination} from device {device.hostname} unsuccessful')
                else:
                    test_results[device.hostname]["Passed"].append(destination)
                    step.passed(f'Ping {destination} from device {device.hostname} successful')

    @aetest.cleanup
    def disconnect(self, testbed):
        '''
        Cleanup after the ping test by disconnecting from all testbed devices.
        '''
        testbed.disconnect()

def make_ping_test(testbed_path:str, destinations:tuple)->tuple:
    '''
    Function to make the ping test. This function calls aetest.main to run the PingTestcase. The
    aetest.main returns the result of the full test including all the testcases. This means that
    even if only one section of one testcase fails, the full test have failed. In addition to the
    status of the full test, we collect summarized details in a dictionary test_results to
    understand what exactly failed. The return value of make_ping_test function includes both
    overal test boolean value, as well as the dictionary of the test_results, for example:
        (Failed, {"Device-1": {"Passed": ['208.67.222.222'], "Failed": ['173.30.1.1']}})

    The summary of results can be collected to the test_results dictionary because a Dictionary is
    a mutable Python structure. This means that the changes done to it in the tests are saved into
    the same dictionary that has been initialized in the make_ping_test function.
    '''
    summary_test_results = {}
    testbed = topology.loader.load(testbed_path)
    ping_test = aetest.main(
                            testable=__name__,
                            testbed=testbed,
                            destinations=destinations,
                            test_results=summary_test_results
                        )
    return (ping_test, summary_test_results)

if __name__ == "__main__":
    my_testbed = "testbed.yaml"
    my_destinations = ('208.67.222.222', '173.30.1.1')
    my_ping_test = make_ping_test(my_testbed, my_destinations)
    print(my_ping_test)
