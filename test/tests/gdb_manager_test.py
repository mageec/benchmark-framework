import unittest
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.gdb_manager import GdbManager
from mock import patch

class MockLogger:
    def log_info(self, sender, msg):
        pass

    def log_warn(self, sender, msg):
        pass

    def log_erro(self, sender, msg):
        pass

class MockPlatform:
    def __init__(self, runner_name="test.runner", name="platform"):
        self.runner_name = runner_name
        self.name = name

    def __str__(self):
        return self.name

class MockGoodRunner:
    def run(self, binary_name, run, results_callback):
        pass

    def ping(self):
        return True

class MockBadRunner(MockGoodRunner):
    def ping(self):
        return False

class TestGdbManager(unittest.TestCase):
    def setUp(self):
        self.logger = MockLogger()
        self.good_runner = MockGoodRunner()
        self.bad_runner = MockBadRunner()
        self.platform = MockPlatform()
        self.gdb_manager = None

    def testLoggerExists(self):
        self.gdb_manager = GdbManager([], self.logger)
        self.assertEqual(self.logger, self.gdb_manager.logger)

    @patch('Pyro4.Proxy')
    def testSuccessfullyInitialisesRunners(self, test_patch):
        test_patch.return_value = self.good_runner
        self.gdb_manager = GdbManager([self.platform], self.logger)
        self.assertEqual({ str(self.platform) : self.good_runner }, self.gdb_manager.runners)

    @patch('Pyro4.Proxy')
    def testSanityPassesIfRunnersPass(self, test_patch):
        test_patch.return_value = self.good_runner
        self.gdb_manager = GdbManager([self.platform], self.logger)
        self.assertTrue(self.gdb_manager.sanity())

    def testSanityFailsIfARunnerFails(self):
        self.gdb_manager = GdbManager([self.platform], self.logger)
        self.gdb_manager.runners['bad_test'] = MockBadRunner()
        self.assertFalse(self.gdb_manager.sanity())

    def testReadEnergyHandlesNonExistentPlatforms(self):
        pass

    def testReadEnergyHandlesNoneExistentBinaries(self):
        pass

if __name__ == '__main__':
    unittest.main()
