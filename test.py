from result import Result
from results import Results

class Test(object):
    def __init__(self, arch, program):
        self.arch = arch
        self.program = program
        self.results = Results(program, str(arch), type(self).__name__)
        self.success = False
        self.error = ""

    def run(self, callback=None):
        logger._write("Test has not been fully implemented.\nSkipping test.")

    def log_results(self, logger):
        logger._write("Test has not been fully implemented.\nSkipping test.")

    def test_callback(self, return_code, err_msg):
        self.success = (return_code == 0)
        self.__error_append(err_msg)

    def error_append(self, err_msg):
        if self.error == "":
            self.error = err_msg
        elif err_msg != "":
            self.error += "\n" + err_msg
        return self.error

    __error_append = error_append
