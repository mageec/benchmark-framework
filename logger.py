import time
import os.path
import sys

class Logger:
    def __init__(self, file_loc='./results_log.txt', quiet=False):
        self.file_loc = os.path.abspath(file_loc)
        self.quiet = quiet
        to_write = "Tests started at: " + self._pretty_print_now()
        self._write(to_write, 'w')

    def write_program_header(self, program):
        self._write("\n***** Results for {} *****".format(program))

    def write_test_header(self, header):
        self._write("*** " + header + " ***")

    def log_results(self, results):
        self._write(str(results))

    def end_log(self):
        to_log = "\nTests finished at: "
        to_log += self._pretty_print_now()
        self._write(to_log)

    @staticmethod
    def _pretty_print_now():
        return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

    def _write(self, to_write, file_mode='a'):
        self.log_file = open(self.file_loc, file_mode)
        self.log_file.write(to_write + "\n")
        if not self.quiet:
            sys.stdout.write(to_write + "\n")
        self.log_file.close()
