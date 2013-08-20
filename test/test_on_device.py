import io
import Pyro4

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import logger
import builder
import gdb_manager
import benchmark
import platform_struct

#export PYRO_HMAC_KEY=Sup3rS3cr3tK3y
#python -Wignore -m Pyro4.naming
#arm-none-eabi-gdb -ex='source /path/to/src/gdb_runners/arm_runner.py'

def main():
    compiler = 'gcc-current'
    with logger.Logger(db='db/test.sqlite3') as logger_obj:
        platform = platform_struct.Platform('arm-none-eabi', { compiler : 'arm-none-eabi-gcc' }, { compiler : '-std=c99 -g -DARM -Tstm32vl_flash.ld -mcpu=cortex-m3 -mthumb exit.c platformcode.c' }, 'runners.arm')
        gdb_manager_obj = gdb_manager.GdbManager([platform], logger_obj)
        if not gdb_manager_obj.sanity():
            print("Cannot access GDB runner")
            return
        builder_obj = builder.Builder(logger_obj, gdb_manager_obj)

        benchmark_obj = benchmark.Benchmark('testProg', { compiler : 'test_prog.c -o testProg' })
        results = builder_obj.build_and_run(benchmark_obj, compiler, platform, [])
        logger_obj.record_results(results)
        print("Completed")


if __name__ == '__main__':
    main()
