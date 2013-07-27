import time

from test import Test

class Speed_Test(Test):

    def run(self, callback=None):
        if callback is None:
            callback = self.test_callback

        if not self.arch.prepare_program(callback):
            return

        for i in range(0, 10):
            start = time.time()
            self.arch.run_program(self.program, callback)
            if not self.success:
                return
            self.results.append(time.time() - start)

    def log_results(self, logger):
        logger.write_test_header("Execution times for {} (in seconds)".format(self.arch.name))
        if self.success:
            if len(self.results) < 0:
                avg_time = 0
            else:
                avg_time = sum(self.results) / len(self.results)
            to_write = "Average execution time: {}".format(str(avg_time))
            for total in self.results:
                to_write += "\n"
                to_write += str(total)
            logger._write(to_write)
        else:
            logger._write(self.error_append("Skipping test."))
