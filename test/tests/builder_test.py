import unittest
from unittest import mock
from mock import patch
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.builder import Builder

class MockLogger:
    def log_info(self, sender, msg):
        pass

    def log_warn(self, sender, msg):
        pass

    def log_erro(self, sender, msg):
        pass

    def add_run(self, benchmark, compiler, platform, flags):
        pass

class MockGdbManager:
    pass

class MockRunner:
    pass

class MockPlatform:
    pass

class MockBenchmark:
    def __init__(self):
        self.name = "MockBenchmark"

class MockPopen:
    def __init__(self, returncode=0):
        self.returncode = returncode

    def communicate(self):
        return ("make_out", "make_err")

class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.logger = MockLogger()
        self.logger.record_results = mock.MagicMock()
        self.gdb_manager = MockGdbManager()
        self.runner = MockRunner()
        self.runner.run_binary = mock.MagicMock()
        self.builder = Builder(self.logger, None, self.runner)
        self.platform = MockPlatform()
        self.platform.name = "TestPlatform"
        self.platform.compiler_bin_for = mock.MagicMock(return_value='gcc')
        self.platform.build_flags_for = mock.MagicMock(return_value='-std=c99 -DARM')
        self.benchmark = MockBenchmark()
        self.benchmark.name = "TestBenchmark"
        self.benchmark.build_flags_for = mock.MagicMock(return_value='test.c -o test')

    def testLoggerExists(self):
        self.assertEqual(self.logger, self.builder.logger)

    def testBuildAndRunDoesNotFailIfNoCompilerIsConfigured(self):
        self.platform.compiler_bin_for = mock.MagicMock(return_value=None)
        self.builder.build_and_run(self.benchmark, 'gcc', self.platform, [])

    def testBuildAndRunDoesNotFailIfNoCompilerBuildFlagsAreConfigured(self):
        self.platform.build_flags_for = mock.MagicMock(return_value=None)
        self.builder.build_and_run(self.benchmark, 'gcc', self.platform, [])

    def testBuildAndRunDoesNotFailIfNoBuildFlagsAreConfigured(self):
        self.benchmark.build_flags_for = mock.MagicMock(return_value=None)
        self.builder.build_and_run(self.benchmark, 'gcc', self.platform, [])

    def testBuildAndRunDoesNotFailIfCompilerDoesNotExist(self):
        self.platform.compiler_bin_for = mock.MagicMock(return_value='NotARealCompiler23')
        self.builder.build_and_run(self.benchmark, 'gcc', self.platform, [])

    @patch('subprocess.Popen')
    def testBuildAndRunDoesNotFailIfCompilationFails(self, test_patch):
        test_patch.return_value = MockPopen(1)
        self.builder.build_and_run(self.benchmark, 'gcc', self.platform, [])

    def testBuildAndRunDoesNotFailIfDirectoryDoesNotExist(self):
        self.builder.build_and_run(self.benchmark, 'gcc', self.platform, [])

    @patch('os.chdir')
    @patch('subprocess.Popen')
    def testBuildAndRunRunsBinary(self, test_patch_subprocess, test_patch_os):
        test_patch_subprocess.return_value = MockPopen()
        test_patch_os = None
        old_num_calls = len(self.runner.run_binary.call_args_list)
        self.builder.build_and_run(self.benchmark, 'gcc', self.platform, [])
        self.assertEqual(1, len(self.runner.run_binary.call_args_list) - old_num_calls)

if __name__ == '__main__':
    unittest.main()
