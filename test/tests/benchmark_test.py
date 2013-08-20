import unittest
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.benchmark import Benchmark

class TestBenchmark(unittest.TestCase):
    def setUp(self):
        self.benchmark = Benchmark("2dfir", {'gcc' : "fir2dim.c"})

    def testNameExists(self):
        self.assertEqual("2dfir", self.benchmark.name)

    def testBuildFlagsExists(self):
        self.assertEqual("fir2dim.c", self.benchmark.build_flags['gcc'])

#TODO: __str__

if __name__ == '__main__':
    unittest.main()
