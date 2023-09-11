from unittest import TestCase, expectedFailure
from buildingblocks.automation_log import AutomationLog
from buildingblocks.SmartJsonConfig.SmartJsonConfig import SmartJsonConfig
import os

class test_smart_json_config(TestCase):
    def setUp(self):
        self._logname = 'SmartJsonConfigTest'
        self._automationlogInstance = AutomationLog(self._logname)
        self._logFilename = self._automationlogInstance.GetFileName()
        self.assertTrue(os.path.isfile(self._logFilename))
        self._logger = self._automationlogInstance.GetLogger(self._logname)
        self._automationlogInstance.TryAddConsole(self._logname)
        self.assertFalse(self._logger is None)
        self._config = SmartJsonConfig('./EdkIIConfig.json')
        pass


    def tearDown(self) -> None:
        pass

    def testLoadJson(self):
        self._logger.info('I am feeling lucky today.')
        pass
