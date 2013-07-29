benchmark-framework
===================

benchmark-framework is a simple framework that automatically run a series of
tests on a set of benchmarks, optionally for different architectures
and/or build conditions.


## Installation ##
### Prerequisites ###
python-yaml

The framework is tested as working on both python 2.7.5 and python 3.3.2.

### Setup ###
Firstly `git clone` the framework to a folder of choice.
Then configure the benchmarks, architectures, and tests by editing `config.yml`.

Note: The framework is currently configured to run the benchmarks on the host
(x86) machine and an ARM board (via gdb and st-link).
The ARM architecture has such different behaviour that a separate 'Architecture'
class had to be written for it. This can be seen in `arch.py`.

## Usage ##
Simply run the `compare.py` script in the directory that contains the
directories of all of the benchmark programs.


## Quirks ##
Each benchmark must reside in a folder that is named the same as the benchmark.
eg. The 'blowfish' benchmark should reside in the 'blowfish' folder.

The binaries for each architecture should be produced with `make <arch>_` in the
folder of the benchmark. This behaviour can be changed in `arch.py`.

The produced binaries should be named `<arch>_<benchmark_name>`.
eg. An x86 binary for 'blowfish' should be called `x86_blowfish`.


## TODO ##
Remove calls to logger._write so we could potentially replace the logger with
one that writes to a database.

Make subprocess calls timeout.

The tests array's in the 'tests' part of the config isn't used at the moment
