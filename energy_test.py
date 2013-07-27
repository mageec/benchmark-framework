import os

from test import Test

class Energy_Test(Test):

    def run(self, program, callback=None):
        if callback is None:
            callback = self.test_callback

        if self.arch.prepare_program(callback):
            self.arch.run_program(self.program, callback)

        if self.success:
            try:
                os.rename('output_results', self.results_file())
            except OSError:
                self.success = False
                if not os.path.isfile('output_results'):
                    self.error_append("No results file found!")
                else:
                    self.error_append("Something went wrong with the test!")

    def log_results(self, logger):
        logger.write_test_header("Energy Monitor results for {}".format(self.arch.name))
        if self.success:
            logger._write("Results saved in {}/{}".format(os.getcwd(),
                    self.results_file()))
        else:
            logger._write(self.error_append("Skipping test."))

    def results_file(self):
        return self.arch.name + "_energy_results.txt"
