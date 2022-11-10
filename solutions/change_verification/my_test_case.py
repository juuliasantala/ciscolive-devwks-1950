from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# List of addresses to ping:
ping_list = ['8.8.8.8', '10.0.0.4']

###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed):
        """
        First setup task: connect to all devices in the testbed

        :param testbed: Testbed object passed as a parameter from the Easypy
            job file.

        :return: None (no return)
        """
        testbed.connect(log_stdout=False)


    # @aetest.subsection
    # def mark_tests_for_looping(self, testbed):  # , perform_configuration):
    #     """
    #     The test will be executed against every device in the testbed, so
    #     define a variable named "device_name" which stores the list of
    #     devices from the testbed.

    #     Each iteration of the marked Testcase will be passed the parameter
    #     "device_name" with the current device's testbed object name.

    #     :param testbed: Testbed object passed as a parameter from the Easypy
    #         job file.

    #     :return: None (no return)
    #     """

    #     aetest.loop.mark(TestNTP, device_name=testbed.devices)

###################################################################
#                     TESTCASES SECTION                           #
###################################################################

class ping_class(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        """ Make sure devices can ping a list of addresses. """
        self.ping_results = {}
        for device_name, device in testbed.devices.items():
            self.ping_results[device_name] = {}
            for ip in ping_list:
                try:
                    print(f"pinging {device}!")
                    ping = device.ping(ip)
                    pingSuccessRate = ping[(ping.find('percent')-4):ping.find('percent')].strip()
                    self.ping_results[device_name][ip] = int(pingSuccessRate)
                except:
                    self.ping_results[device_name][ip] = 0

    @aetest.test
    def test(self, steps):
        # Loop over every ping result
        for device_name, ips in self.ping_results.items():
            with steps.start(
                f"Looking for ping failures {device_name}", continue_=True
            ) as device_step:
                # Loop over every ping result
                for ip in ips:
                    with device_step.start(
                        f"Checking Ping from {device_name} to {ip}", continue_=True
                    ) as ping_step:
                        if ips[ip] < 100:
                            device_step.failed(
                            f'Device {device_name} had {ips[ip]}% success pinging {ip}')

class CommonCleanup(aetest.CommonCleanup):
    """
    Common cleanup tasks - this class can only be instantiated one time per
    testscript.
    """

    @aetest.subsection
    def disconnect(self, testbed):
        """
        Disconnect from all testbed devices

        :param testbed: Easypy-passed testbed object
        :return: None (no return value)
        """
        testbed.disconnect()


if __name__ == "__main__":
    from pyats import topology
    testbed = "testbed.yaml"
    print(f"loading testbed {testbed}")
    testbed = load(testbed)
    aetest.main(testbed=testbed)
