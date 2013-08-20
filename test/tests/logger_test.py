import unittest
import sys

import io

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()
        self.logger = Logger(log=self.stream, db='db/test.sqlite3')

    def tearDown(self):
        self.stream.close()

    def testCanLogInfo(self):
        self.assertEqual("", self.stream.getvalue())
        with self.logger as logger:
            logger.log_info("testCanLogInfo", "This is a test.")

        self.assertTrue(len(self.stream.getvalue()) > 0)

    def testCanLogWarnings(self):
        self.assertEqual("", self.stream.getvalue())
        with self.logger as logger:
            logger.log_info("testCanLogWarn", "This is a test.")

        self.assertTrue(len(self.stream.getvalue()) > 0)

    def testCanLogErrors(self):
        self.assertEqual("", self.stream.getvalue())
        with self.logger as logger:
            logger.log_erro("testCanLogErro", "This is a test.")

        self.assertTrue(len(self.stream.getvalue()) > 0)

    def testProperlyProcessesThreadedInputs(self):
        pass

    def testResultsAreRecorded(self):
        pass

    def testEmptyResultsDoesNothing(self):
        pass

if __name__ == '__main__':
    unittest.main()
