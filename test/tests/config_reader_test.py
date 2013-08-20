import unittest
import sys

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

import os
import src.config_reader

config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configs'))

class TestConfigReader(unittest.TestCase):
    def setUp(self):
        pass

    def testFunctionalTest(self):
        config_file = os.path.join(config_dir, 'functional.yml')
        flag_file = os.path.join(config_dir, 'functional.csv')
        compilers, platforms, benchmarks, database = src.config_reader.read(config_file, flag_file)

        self.assertEqual(compilers['compiler'], ["flag"])
        self.assertEqual(compilers['other_compiler'], ["other"])

        a_platform = platforms[0] # platform
        o_platform = platforms[1] # other_platform
        a_benchmark = benchmarks[0] # benchmark
        o_benchmark = benchmarks[1] # other_benchmark
        a_compiler = 'compiler'
        o_compiler = 'other_compiler'

        aaa_build_str = a_benchmark.build_flags_for(a_compiler) + ' ' + a_platform.build_flags_for(a_compiler)
        self.assertTrue("(everything)" in aaa_build_str)
        self.assertTrue("(benchmark only)" in aaa_build_str)
        self.assertTrue("(compiler only)" in aaa_build_str)
        self.assertTrue("(platform only)" in aaa_build_str)
        self.assertTrue("(compiler on platform)" in aaa_build_str)
        #self.assertTrue("(benchmark on platform)" in aaa_build_str)
        self.assertTrue("(benchmark with compiler)" in aaa_build_str)
        #self.assertTrue("(each only)" in aaa_build_str)

        oaa_build_str = o_benchmark.build_flags_for(a_compiler) + ' ' + a_platform.build_flags_for(a_compiler)
        self.assertTrue("(everything)" in oaa_build_str)
        self.assertFalse("(benchmark only)" in oaa_build_str)
        self.assertTrue("(compiler only)" in oaa_build_str)
        self.assertTrue("(platform only)" in oaa_build_str)
        self.assertTrue("(compiler on platform)" in oaa_build_str)
        #self.assertFalse("(benchmark on platform)" in oaa_build_str)
        self.assertFalse("(benchmark with compiler)" in oaa_build_str)
        #self.assertFalse("(each only)" in oaa_build_str)

        aoa_build_str = a_benchmark.build_flags_for(a_compiler) + ' ' + o_platform.build_flags_for(a_compiler)
        self.assertTrue("(everything)" in aoa_build_str)
        self.assertTrue("(benchmark only)" in aoa_build_str)
        self.assertTrue("(compiler only)" in aoa_build_str)
        self.assertFalse("(platform only)" in aoa_build_str)
        self.assertFalse("(compiler on platform)" in aoa_build_str)
        #self.assertFalse("(benchmark on platform)" in aoa_build_str)
        self.assertTrue("(benchmark with compiler)" in aoa_build_str)
        #self.assertFalse("(each only)" in aoa_build_str)

        aao_build_str = a_benchmark.build_flags_for(o_compiler) + ' ' + a_platform.build_flags_for(o_compiler)
        self.assertTrue("(everything)" in aao_build_str)
        self.assertTrue("(benchmark only)" in aao_build_str)
        self.assertFalse("(compiler only)" in aao_build_str)
        self.assertTrue("(platform only)" in aao_build_str)
        self.assertFalse("(compiler on platform)" in aao_build_str)
        #self.assertTrue("(benchmark on platform)" in aao_build_str)
        self.assertFalse("(benchmark with compiler)" in aao_build_str)
        #self.assertFalse("(each only)" in aao_build_str)

        aoo_build_str = a_benchmark.build_flags_for(o_compiler) + ' ' + o_platform.build_flags_for(o_compiler)
        self.assertTrue("(everything)" in aoo_build_str)
        self.assertTrue("(benchmark only)" in aoo_build_str)
        self.assertFalse("(compiler only)" in aoo_build_str)
        self.assertFalse("(platform only)" in aoo_build_str)
        self.assertFalse("(compiler on platform)" in aoo_build_str)
        #self.assertFalse("(benchmark on platform)" in aoo_build_str)
        self.assertFalse("(benchmark with compiler)" in aoo_build_str)
        #self.assertFalse("(each only)" in aoo_build_str)

        oao_build_str = o_benchmark.build_flags_for(o_compiler) + ' ' + a_platform.build_flags_for(o_compiler)
        self.assertTrue("(everything)" in oao_build_str)
        self.assertFalse("(benchmark only)" in oao_build_str)
        self.assertFalse("(compiler only)" in oao_build_str)
        self.assertTrue("(platform only)" in oao_build_str)
        self.assertFalse("(compiler on platform)" in oao_build_str)
        #self.assertFalse("(benchmark on platform)" in oao_build_str)
        self.assertFalse("(benchmark with compiler)" in oao_build_str)
        #self.assertFalse("(each only)" in oao_build_str)

        ooa_build_str = o_benchmark.build_flags_for(a_compiler) + ' ' + o_platform.build_flags_for(a_compiler)
        self.assertTrue("(everything)" in ooa_build_str)
        self.assertFalse("(benchmark only)" in ooa_build_str)
        self.assertTrue("(compiler only)" in ooa_build_str)
        self.assertFalse("(platform only)" in ooa_build_str)
        self.assertFalse("(compiler on platform)" in ooa_build_str)
        #self.assertFalse("(benchmark on platform)" in ooa_build_str)
        self.assertFalse("(benchmark with compiler)" in ooa_build_str)
        #self.assertFalse("(each only)" in ooa_build_str)

        ooo_build_str = o_benchmark.build_flags_for(o_compiler) + ' ' + o_platform.build_flags_for(o_compiler)
        self.assertTrue("(everything)" in ooo_build_str)
        self.assertFalse("(benchmark only)" in ooo_build_str)
        self.assertFalse("(compiler only)" in ooo_build_str)
        self.assertFalse("(platform only)" in ooo_build_str)
        self.assertFalse("(compiler on platform)" in ooo_build_str)
        #self.assertFalse("(benchmark on platform)" in ooo_build_str)
        self.assertFalse("(benchmark with compiler)" in ooo_build_str)
        #self.assertFalse("(each only)" in ooo_build_str)

if __name__ == '__main__':
    unittest.main()
