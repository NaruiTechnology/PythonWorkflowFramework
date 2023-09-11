import sys, os
sys.path.append(os.path.split(os.path.dirname(os.getcwd()))[0])
import unittest
import buildingblocks.SmartJsonConfig.unittest_smart_json_config.test_smart_json_config as tsSmartJsonConfig
import buildingblocks.BinaryDocker.unitest_binary_docker.test_binary_docker as tsBinaryDockerr

loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTest(loader.loadTestsFromModule(tsSmartJsonConfig))
suite.addTest(loader.loadTestsFromModule(tsBinaryDockerr))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
