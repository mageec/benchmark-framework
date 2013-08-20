import unittest
import sys

import os
import random
import shutil
import sqlite3
import string

sys.path.append("../") # Go up one if run in the test suite
sys.path.append("../../") # Go up two if run directly

from src.dbi import DBi

class TestDBi(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.abspath(os.path.join(__file__, '..'))
        self.db_loc = os.path.join(self.root_dir, 'db/test.sqlite3')

    def tearDown(self):
        shutil.rmtree(os.path.join(self.root_dir, 'db'), ignore_errors=True)

# __init__
#TODO: Check DB contents are setup
    def testDbIsCreatedIfItDoesNotExist(self):
        self.assertFalse(os.path.isfile(self.db_loc))
        try:
            os.mkdir('db')
        except OSError:
            pass

        dbi = DBi(self.db_loc)
        self.assertTrue(os.path.isfile(self.db_loc))

#TODO: Check DB contents are setup
    def testDbIsCreatedIfItAndFolderDoesNotExist(self):
        self.assertFalse(os.path.isdir(os.path.join(self.root_dir, 'db')))
        self.assertFalse(os.path.isfile(self.db_loc))

        dbi = DBi(self.db_loc)
        self.assertTrue(os.path.isfile(self.db_loc))

# fetch
    def testFetchedResultsAreNotReturnedIfNoneExist(self):
# Seed DB with a run that has different flags, and results for it
# Check a similar run that has no results
        pass

    def testOldResultsCanBeFetched(self):
        expected_results = [(1, 2), (3, 4)]
        dbi = DBi(self.db_loc)
        benchmark = "bm"
        compiler = "gcc"
        platform = "arm"
        flags = ["-a-flag"]
        run = self.run_factory(dbi, flags, benchmark, compiler, platform)
        self.result_factory(dbi, run, expected_results)

        self.assertEqual(expected_results, dbi.fetch(run))

# record
    def testResultsCanBeRecorded(self):
        expected_results = [(1, 2), (3, 4)]
        expected_results.sort()
        dbi = DBi(self.db_loc)
        run_id = self.run_factory(dbi)
        with dbi:
            dbi.record(run_id, expected_results)

        with dbi:
            dbi.cursor.execute("SELECT time, energy FROM results WHERE run_id = ?;", (run_id,))
            out_results = dbi.cursor.fetchall()
            out_results.sort()

        self.assertEqual(expected_results, out_results)

    def testRecordingEmptyResultsDoesNotCommitOrFail(self):
        dbi = DBi(self.db_loc)
        run_id = self.run_factory(dbi)
        with dbi:
            dbi.record(run_id, [])

        with dbi:
            dbi.cursor.execute("SELECT time, energy FROM results WHERE run_id = ?;", (run_id,))
            out_results = dbi.cursor.fetchall()

        self.assertEqual([], out_results)

# add_run
    def testANewRunWithNoFlagsGetsANewId(self):
        dbi = DBi(self.db_loc)
        flags = []
        benchmark = "bm"
        compiler = "gcc"
        platform = "arm"
        other_run_id = self.run_factory(dbi, ["-a-flag"], benchmark, compiler, platform)
        run_id = self.run_factory(dbi, flags, benchmark, compiler, platform)

        self.assertNotEqual(other_run_id, run_id)

    def testANewRunWithLessFlagsGetsANewId(self):
        dbi = DBi(self.db_loc)
        flags = ["-a-flag", "-b-flag", "-c-flag"]
        benchmark = "bm"
        compiler = "gcc"
        platform = "arm"
        other_run_id = self.run_factory(dbi, flags, benchmark, compiler, platform)
        flags.remove("-b-flag")
        run_id = self.run_factory(dbi, flags, benchmark, compiler, platform)

        self.assertNotEqual(other_run_id, run_id)

    def testANewRunWithMoreFlagsGetsANewId(self):
        dbi = DBi(self.db_loc)
        flags = ["-a-flag", "-b-flag"]
        benchmark = "bm"
        compiler = "gcc"
        platform = "arm"
        other_run_id = self.run_factory(dbi, flags, benchmark, compiler, platform)
        flags += "-c-flag"
        run_id = self.run_factory(dbi, flags, benchmark, compiler, platform)

        self.assertNotEqual(other_run_id, run_id)
        pass

# __setup_db

# __db_dir_exists

# __db_is_setup

# __gen_run_id

# __existing_run
# Tested by add_run tests

# __create_run
# Tested by add_run tests

# Threading
# TODO: Implement and test for threading inputs
# Could test for using multiple DBis on the same database but currently we don't
# guarantee this behaviour

# Factories
    def run_factory(self, dbi, flags=[], benchmark=None, compiler=None, platform=None):
        if benchmark is None:
            benchmark = self.gen_random_string()
        if compiler is None:
            compiler = self.gen_random_string()
        if platform is None:
            platform = self.gen_random_string()

        with dbi:
            dbi.cursor.execute("INSERT INTO runs(benchmark, compiler, platform) VALUES (?, ?, ?);", (benchmark, compiler, platform))
            run_id = dbi.cursor.lastrowid
            for flag in flags:
                dbi.cursor.execute("INSERT INTO flags(flag) VALUES (?);", (flag,))
                flag_id = dbi.cursor.lastrowid
                dbi.cursor.execute("INSERT INTO run_flags VALUES (?, ?);", (run_id, flag_id))
            dbi.connection.commit()

        return run_id

    def result_factory(self, dbi, run_id, results):
        with dbi:
            for result in results:
                dbi.cursor.execute("INSERT INTO results(run_id, time, energy) VALUES (?, ?, ?);", (run_id, result[0], result[1]))
                dbi.connection.commit()

    def gen_random_string(self, length=10):
        return ''.join([random.choice(string.ascii_lowercase) for _ in range(0, length)])

if __name__ == '__main__':
    unittest.main()
