import unittest
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.module import Module

class TestModule(unittest.TestCase):
    def setUp(self):
        self.module = Module()

# Tests...

if __name__ == '__main__':
    unittest.main()
