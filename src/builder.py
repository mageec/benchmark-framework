import subprocess

import os
import sys
sys.path.append(os.path.dirname(__file__))

import run
import runner

class Builder:
    def __init__(self, logger, gdb_manager, runner_obj=None):
        self.logger = logger
        if runner_obj is None:
            self.runner = runner.Runner(logger, gdb_manager)
        else:
            self.runner = runner_obj

    def build_and_run(self, benchmark, compiler, platform, flags):
        compiler_bin  = platform.compiler_bin_for(compiler)
        build_flags = platform.build_flags_for(compiler)
        bm_build_flags = benchmark.build_flags_for(compiler)
        if compiler_bin is None:
            self.logger.log_warn("builder", "No {} compiler binary configured for {}".format(compiler, str(platform)))
            return
        if build_flags is None:
            self.logger.log_warn("builder", "No {} build flags configured for {}".format(compiler, str(platform)))
            return
        if bm_build_flags is None:
            self.logger.log_warn("builder", "No {} benchmark build flags configured for {}".format(compiler, str(platform)))
            return

        to_run  = [compiler_bin]
        to_run += build_flags.split()
        to_run += flags
        to_run += bm_build_flags.split()
        try:
            os.chdir(benchmark.name)
        except FileNotFoundError:
            self.logger.log_warn("builder", "Cannot find {} directory".format(benchmark.name))
            return

        try:
            self.logger.log_info("builder", "Executing {}".format(" ".join(to_run)))
            p = subprocess.Popen(to_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            make_out, make_err = p.communicate()
        except FileNotFoundError:
            self.logger.log_warn("builder", "Cannot find compiler ({}) for {}.".format(compiler_bin, str(platform)))
            return
        finally:
            os.chdir('..')

        if p.returncode != 0:
            self.logger.log_warn("builder", "Build failed for {} using {}.".format(str(platform), compiler))
            self.logger.log_warn("builder", "{}\n{}".format(make_out.decode("utf-8"), make_err.decode("utf-8")))
            return

        run_id = self.logger.add_run(benchmark.name, compiler, platform.name, flags)
        run_obj = run.Run(benchmark, compiler, platform, flags, run_id)
        return self.runner.run_binary(os.path.join(benchmark.name, benchmark.name), run_obj)
