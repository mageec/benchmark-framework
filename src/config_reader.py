from os import path
from yaml import load
try:
        from yaml import CLoader as Loader
except ImportError:
        from yaml import Loader

import sys
sys.path.append(path.dirname(__file__))

import benchmark
import platform_struct

def read(config_file=
        path.abspath(path.join(path.dirname(__file__), '..', 'config.yml')),
         flag_config_file=
        path.abspath(path.join(path.dirname(__file__), '..', 'config.csv'))):
    #TODO: Speed up and tidy up
    compilers = {}
    platforms = []
    benchmarks = []
    with open(config_file, 'r') as f:
        config = load(f)

    database = config['database']

    all_compilers = []
    for compiler in config['compilers']:
        compilers[compiler['name']] = compiler['flags']
        all_compilers.append(compiler['name'])

    for platform_cfg in config['platforms']:
        try:
            poss_compilers = platform_cfg['compiler_whitelist']
        except KeyError:
            poss_compilers = all_compilers

        try:
            not_compilers = platform_cfg['compiler_blacklist']
        except KeyError:
            not_compilers = []

        for to_remove in not_compilers:
            #TODO: Catch error
            poss_compilers.remove(to_remove)

        compiler_bins = {}
        build_flags = {}
        for compiler in poss_compilers:
            try:
                compiler_bins[compiler] = platform_cfg[compiler]
                build_flags[compiler] = ""
            except KeyError:
# Do nothing and don't compile with this compiler
                pass

        platforms.append(platform_struct.Platform(
            platform_cfg['name'],
            compiler_bins,
            build_flags,
            platform_cfg['runner_name']
            ))

    for benchmark_cfg in config['benchmarks']:
        try:
            poss_compilers = benchmark_cfg['compiler_whitelist']
        except KeyError:
            poss_compilers = all_compilers

        try:
            not_compilers = benchmark_cfg['compiler_blacklist']
        except KeyError:
            not_compilers = []

        for to_remove in not_compilers:
            #TODO: Catch error
            poss_compilers.remove(to_remove)

        build_flags = {}
        for compiler in poss_compilers:
            build_flags[compiler] = ""

        benchmarks.append(benchmark.Benchmark(benchmark_cfg['name'], build_flags))

    with open(flag_config_file, 'r') as flag_config:
        for line in flag_config:
            cfg = line.split(',', 3)
            cfg[3] = cfg[3].strip()
            if cfg[0] == '*' and cfg[1] == '*' and cfg[2] == '*':
                for platform_obj in platforms:
                    for compiler in platform_obj.compilers:
                        try:
                            platform_obj.build_flags[compiler] += ' ' + cfg[3]
                        except KeyError:
# We should compile using this compiler, so ignore this error
                            pass
            elif cfg[1] == '*' and cfg[2] == '*':
                for benchmark_obj in benchmarks:
                    if benchmark_obj.name == cfg[0]:
                        for compiler in benchmark_obj.build_flags:
                            benchmark_obj.build_flags[compiler] += ' ' + cfg[3]
                        break
            elif cfg[0] == '*' and cfg[2] == '*':
                for benchmark_obj in benchmarks:
                    try:
                        benchmark_obj.build_flags[cfg[1]] += ' ' + cfg[3]
                    except KeyError:
# We should compile using this compiler, so ignore this error
                        pass
            elif cfg[0] == '*' and cfg[1] == '*':
                for platform_obj in platforms:
                    if platform_obj.name == cfg[2]:
                        for compiler in platform_obj.compilers:
                            platform_obj.build_flags[compiler] += ' ' + cfg[3]
                    break
            elif cfg[0] == '*':
                for platform_obj in platforms:
                    if platform_obj.name == cfg[2]:
                        try:
                            platform_obj.build_flags[cfg[1]] += ' ' + cfg[3]
                        except KeyError:
# We should not compile using this compiler, so ignore this error
                            pass
            elif cfg[1] == '*':
                #TODO: Implement support for this in the data structures
                pass
            elif cfg[2] == '*':
                for benchmark_obj in benchmarks:
                    if benchmark_obj.name == cfg[0]:
                        try:
                            benchmark_obj.build_flags[cfg[1]] += ' ' + cfg[3]
                        except KeyError:
# We should not compile using this compiler, so ignore this error
                            pass
                    break
            else:
                #TODO: Implement support for this in the data structures
                pass

    return (compilers, platforms, benchmarks, database)
