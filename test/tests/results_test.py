import unittest
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.results import Results

class MockRun:
    pass

class TestModule(unittest.TestCase):
    def setUp(self):
        self.run = MockRun()
        self.results = Results(self.run)

    def testResultsIsEmptyBeforeRecorded(self):
        self.assertEqual([], self.results.results)

    def testValidResultsCanBeRecorded(self):
        self.results.record_result(50, 0.10834)
        self.results = [(50, 0.10834)]

    def testInvalidResultsRaisesError(self):
        with self.assertRaises(AttributeError):
            self.results.record_result(50.1, 0.1)
        self.assertEqual([], self.results.results)

    def testCanBeInitialisedWithResults(self):
        results = [(34234, 32084)]
        self.results = Results(self.run, results)
        self.assertEqual(results, self.results.results)

    def testReturnCodeIsNoneBeforeRecorded(self):
        self.assertIsNone(self.results.return_code)

    def testReturnCodeCanBeRecorded(self):
        self.results.return_code = 1
        self.assertEqual(1, self.results.return_code)

    def testCanAccessRun(self):
        self.assertEqual(self.run, self.results.run)

# TODO: __str__

if __name__ == '__main__':
    unittest.main()
