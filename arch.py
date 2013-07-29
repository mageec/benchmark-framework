import os
import subprocess
import threading

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

    def run_program(self, program, callback):
        def target():
            self.process = subprocess.Popen(["./{}_{}".format(self.name, program)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.process.communicate()

        def terminator():
            self.process.terminate()

        def return_coder():
            return self.process.returncode

        return_code = self._safe_run(target, terminator, return_coder)
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
        elif (return_code == -2):
            callback(return_code, "Program timed out.")
        elif (return_code != 0):
            callback(return_code, "Program did not exit correctly.")
        else:
            callback(0, "")

    def _safe_run(self, target, terminator, return_code_accessor, timeout=120):
        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            terminator()
            thread.join()
            return -2
        return return_code_accessor()

    def __str__(self):
        return self.name


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
        def target():
            self.process = subprocess.Popen(["arm-none-eabi-gdb", "-ex=source {}".format(script)] + extra_flags + ["-ex=quit 1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.process.communicate()

        def terminator():
            self.process.terminate()

        def return_coder():
            return self.process.returncode

        to_return = self._safe_run(target, terminator, return_coder)
        return to_return
