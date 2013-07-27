import os
import yaml

import arch
from logger import Logger
from program import Program

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yml")
config = yaml.load(open(config_file, 'r'))
logger = Logger()

def init_archs(archs):
    to_return = []
    for arch_name in archs:
       if arch_name == "arm":
          to_return.append(arch.Arm(arch_name, config['tests'][arch_name]))
       else:
          to_return.append(arch.Architecture(arch_name, config['tests'][arch_name]))
    return to_return

def main():
    work_dir = os.getcwd()
    for program_cfg in config['programs']:
        logger.write_program_header(program_cfg['name'])
        try:
            os.chdir(program_cfg['name'])
        except OSError:
            to_write = "Directory for {} does not exist.".format(program_cfg['name'])
            to_write += "\nSkipping tests."
            logger._write(to_write)
            continue
        archs = init_archs(program_cfg['archs'])
        program = Program(program_cfg['name'], archs)
        program.run_tests(logger)
        os.chdir(work_dir)
    logger.end_log()

if __name__ == '__main__':
    main()
