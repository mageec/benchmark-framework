import unittest
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.platform_struct import Platform

class TestPlatform(unittest.TestCase):
    def setUp(self):
        self.platform = Platform("arm", {'gcc' : "arm-none-eabi-gcc" }, {'gcc' : "-DARM"}, "runners.arm")

    def testNameExists(self):
        self.assertEqual("arm", self.platform.name)

    def testCompilersExists(self):
        self.assertEqual({ 'gcc' : "arm-none-eabi-gcc" }, self.platform.compilers)

    def testBuildFlagsExists(self):
        self.assertEqual("-DARM", self.platform.build_flags['gcc'])

    def testRunnerNameExists(self):
        self.assertEqual("runners.arm", self.platform.runner_name)

    def testStrIsPlatformName(self):
        self.assertEqual("arm", str(self.platform))

if __name__ == '__main__':
    unittest.main()
