import os
import subprocess

class Architecture(object):
    def __init__(self, name, tests):
        self.name = name
        self.tests = tests
        self.built_bins = False

    def make_binaries(self, callback, extra_flags=[]):
        self.built_bins = False
        subprocess.call(["make", "clean"], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
        p = subprocess.Popen(["make"] + extra_flags + [self.name + "_"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        make_out, make_err = p.communicate()
        if p.returncode != 0:
            err_msg = "make failed!"
            err_msg += "\n" + str(make_out)
            err_msg += "\n" + str(make_err)

            callback(p.returncode, err_msg)
            return False

        self.built_bins = True
        return True

    def prepare_program(self, callback):
        if not self.built_bins:
            return self.make_binaries(callback)
        return True

#TODO: Make subprocess timeout. What if we run forever!?
    def run_program(self, program, callback):
        return_code = subprocess.call(["./{}_{}".format(self.name, program)])
        self._handle_program_exit(return_code, callback)
        return return_code

    def run_tests(self, program, logger, callback=None):
        for test in self.tests:
            mod = __import__(test.lower())
            test_class = getattr(mod, test)
            test = test_class(self, program)
            test.run(callback)
            test.log_results(logger)

    def _handle_program_exit(self, return_code, callback):
        if (return_code == -1):
            callback(return_code, "Program did not produce correct output.")
        elif (return_code != 0):
            callback(return_code, "Program did not exit correctly.")
        else:
            callback(0, "")


class Arm(Architecture):

    def prepare_program(self, callback):
        if not self.built_bins:
# We need debug symbols to determine the return value
            return self.make_binaries(callback, ["DEBUG=1"])
        return True

#TODO: Figure out a way to move loading onto the board into prepare_program
    def run_program(self, program, callback):
        script = os.path.join(os.path.dirname(os.path.realpath(__file__)), "arm_gdb.py")
        return_code = self._run_gdb(script,
                ["-ex=arm_run_program {}".format(program), "-ex=arm_quit_program"])
        self._handle_program_exit(return_code, callback)
        return return_code

    def _run_gdb(self, script, extra_flags=[]):
        return subprocess.call(["arm-none-eabi-gdb", "-ex=source {}".format(script)]
                + extra_flags + ["-ex=quit 1"],
                stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))

