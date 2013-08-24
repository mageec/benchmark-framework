import os
import Pyro4
Pyro4.config.HMAC_KEY=b"Sup3rS3cr3tK3y"

"""import sys
sys.path.append(os.path.dirname(__file__))

import results"""

class GdbManager:
    def __init__(self, platforms, logger):
        logger.log_info("gdb_manager", "Initialising GDB Manager")
        self.logger = logger
        self.runners = {}
        for platform in platforms:
            self.runners[platform.name] = Pyro4.Proxy("PYRONAME:{}".format(platform.runner_name))
        self.logger.log_info("gdb_manager", "Initialized GDB Manager")

    def read_energy(self, binary_name, run):
        #TODO: Parameter checks
        self.logger.log_info("gdb_manager", "Running {} on {}".format(binary_name, run.platform.name))
        runner = self.runners[run.platform.name]

        results = runner.run_binary(os.path.abspath(binary_name), run)
        self.logger.log_info("gdb_manager", "Successfully ran {} on {}".format(binary_name, str(run.platform)))
        #return results.Results(result_ary[0], result_ary[1], result_ary[2])
        return results

    def sanity(self):
        for runner in self.runners:
            try:
                self.runners[runner].ping()
                self.logger.log_info("gdb_manager", "Successfully pinged {}".format(runner))
            except:
                self.logger.log_erro("gdb_manager", "Failed to ping {}".format(runner))
                return False
        self.logger.log_info("gdb_manager", "Successfully pinged all runners")
        return True
