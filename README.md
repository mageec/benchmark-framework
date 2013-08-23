benchmark-framework
===================

benchmark-framework is a simple framework that automatically run a series of
benchmarks with different compilers and optimization flags on different
platforms.

## Installation ##
### Prerequisites ###
python-yaml

Pyro4

For running the tests, 'python-mock' is also required.

For the relevant GDB for each platform, Python support must be built into it.

You will also need the pyenergy.so module from
https://github.com/jpallister/stm32f4-energy-monitor
Be sure to build with whatever version of Python is built into the GDB binaries
(and by extension, which version Python the GDB runners are written for).

The framework is tested as working on Python 3.3.2.
It has not been tested on Python 2.x and is unlikely to work on it.

### Setup ###
Firstly `git clone` the framework to a folder of choice.

Then configure the benchmarks, architectures, and compilers by editing
`config.yml`.

Finally, configure which build flags to use by editing `config.csv`.

## Configuration ###
### config.yml ###
* platforms: An array of platform objects.
  * name: The name of the platform. This is used internally and in the database.
  * runner_name: The PYRONAME of the GDB runner for this platform.
  * \<compilers\>: For each compiler you want to use with this platform, you need
    a corresponding entry that configures what compiler binary to use for this
    platform and compiler. It can be a binary name (but must be in PATH), or an
    absolute path to a binary. \<compiler\> is the name of the compiler used in
    the 'compilers' array of this file.
  * compiler_whitelist: An optional whitelist array of compilers to use. By
    default, this is every compiler with a corresponding compiler entry in this
    object.
  * compiler_blacklist: An optional blacklist array of compilers. This overrides
    any entries in compiler_whitelist.

* benchmarks: An array of benchmark objects.
  * name: The name of the benchmark. The benchmark source code should reside in
    a directory with this name. It should also be run with a binary of this
    name.
  * compiler_whitelist: An optional whitelist array of compilers to use. By
    default, this is every compiler with a corresponding compiler entry in this
    object.
  * compiler_blacklist: An optional blacklist array of compilers. This overrides
    any entries in compiler_whitelist.

* compilers: An array of compiler objects.
  * name: The name of the compiler. This is used internally and in the database.
  * flags: An array of optimizations to run each benchmark with. It will be run
    with and without every flag in every combination.

* database:
  * database: Currently the framework is using sqlite, so this is just a
    relative location to the database file. The file will be created if it does
    not exist.

### config.csv ###
Each row in this file specifies a benchmark name, compiler name, platform name,
and what build flags to use for this combination.
Each name should be the same as what's used in `config.yml`.
An asterix can be used in any of the first three fields to indicate any
benchmark, compiler, or platform (dedpending on the field that it's in).

## Usage ##
Change the Pyro HMAC key in `src/gdb_manager.py` and all gdb runners in
`src/gdb_runners`.
Run `export PYRO_HMAC_KEY=<HMAC key>`, where `<HMAC key>` is the key you've just
put into the GDB manager and GDB runners.
in the same terminal, start up a Pyro4 nameserver with `python -m Pyro4.naming`.

Start up each GDB runner in the platform's relevant GDB.

Run the `framework.py` script in the directory that contains the folders of all
the benchmarks.

## Testing ##
Tests can either be run individually with `python tests/<script.py>` (when in
the test directory)
or all together with `python test/suite.py`.

`suite.py` runs all tests in 'test/tests' that end in 'test.py'

`template.py` is just a basic template for any new tests.

## Quirks ##
Each benchmark must reside in a folder that is named the same as the benchmark.
eg. The 'blowfish' benchmark should reside in the 'blowfish' folder.

The produced binaries should be named the same as the benchmark.
eg. The 'blowfish' benchmark should be run with the 'blowfish' binary.

## TODO ##
There are numerous TODOs in the source files that aren't metioned here.

Do more sanity checks in framework.py before running everything. (eg does every
compiler binary exist, does every benchmark directory exist)

Add more tests. Some aren't as extensive as they could be at the moment.

The dbi tests are a bit slow because we're creating and deleting the database
with every test. This could be sped up by just deleting the database contents
instead, and deleting and creating the database directory only in the tests that
need it.

Maybe make the test_on_device test to be more general, and accept more
platforms.

Do more error handling. This is designed to run for potentially days and an
exception will stop it dead currently.

Add support for build flags that are specific to a benchmark and platform.
Currently the config_reader ignores these because it can't be done with the data
structures that exist at the time of writing. It might be worth changing how
build flags are stored in memory all together.

Make all file references (and relevant module imports) relative to the location
of the script making the reference. Currently, some file references are done
relative to the current directory instead.

Make everything threaded. (Specifically the dbi, logger, and gdb_manager). This
will depend on the TODO below.

Read results straight from pyenergy, instead of from the file that it creates.
This will require changes to pyenergy.
An extra issue until then is that pyenergy may not make a new results file for a
new test, and therefore the results in the file could be read by the next test,
instead of the test failing.

Add support for Python 2.x. This shouldn't be too difficult for the main code,
but the tests use quite a bit of Python3-only stuff. Using unittest2 should
help.

Make an easier way to stop each GDB runner than connecting through the Python
interpreter manually.

Move from using Pyro to using GDB/MI instead.

Use expect instead of python inside the gdb runners.

Make programs timeout.
