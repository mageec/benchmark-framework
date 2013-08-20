import os
import sys
sys.path.append(os.path.dirname(__file__))

import itertools

import builder
import config_reader
import gdb_manager
import logger

def main():
    compilers, platforms, benchmarks, database = config_reader.read()
    logger_obj = logger.Logger(db=database['database'])
    gdb_man = gdb_manager.GdbManager(platforms, logger_obj)
    builder_obj = builder.Builder(logger_obj, gdb_man)

    if not gdb_man.sanity():
        logger_obj.log_erro("framework", "GDB Manager failed sanity check.\nExiting")
        return

    for compiler in compilers:
        for a_platform in platforms:
            for a_benchmark in benchmarks:
                flags = compilers[compiler]
                for i in range(0, len(flags) + 1):
                    for flag_set in itertools.combinations(flags, i):
                        results = builder_obj.build_and_run(a_benchmark, compiler, a_platform, flag_set)
                        if results is not None:
                            logger_obj.record_results(results)

if __name__ == "__main__":
    main()
