import unittest
from unittest import mock
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.runner import Runner

class MockLogger:
    pass

class MockGdbManager:
    pass

class TestRunner(unittest.TestCase):
    def setUp(self):
        self.logger = MockLogger()
        self.logger.record_results = mock.MagicMock()
        self.gdb_manager = MockGdbManager()
        self.gdb_manager.read_energy = mock.MagicMock()
        self.runner = Runner(self.logger, self.gdb_manager)

    def testLoggerExists(self):
        self.assertEqual(self.logger, self.runner.logger)

    def testGdbManagerExists(self):
        self.assertEqual(self.gdb_manager, self.runner.gdb_manager)

    def testRunBinaryCallsGdbManager(self):
        old_num_calls = len(self.gdb_manager.read_energy.call_args_list)
        self.runner.run_binary(None, None)
        self.assertEqual(1, len(self.gdb_manager.read_energy.call_args_list) - old_num_calls)

if __name__ == '__main__':
    unittest.main()
