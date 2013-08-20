import unittest
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.run import Run

class TestRun(unittest.TestCase):
    def setUp(self):
        self.run = Run("benchmark", "compiler", "platform", ["flag"], 1)

    def testBenchmarkExists(self):
        self.assertEqual("benchmark", self.run.benchmark)

    def testCompilerExists(self):
        self.assertEqual("compiler", self.run.compiler)

    def testPlatformExists(self):
        self.assertEqual("platform", self.run.platform)

    def testFlagsExists(self):
        self.assertEqual(["flag"], self.run.flags)

    def testIdExists(self):
        self.assertEqual(1, self.run.id)

#TODO: __str__

if __name__ == '__main__':
    unittest.main()
