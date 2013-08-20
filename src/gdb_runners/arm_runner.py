import Pyro4
import sys

sys.excepthook = Pyro4.util.excepthook
Pyro4.config.HMAC_KEY=b"Sup3rS3cr3tK3y"

sys.path.append('')
sys.path.append('..')

import pyenergy
import results

class Arm_Gdb_Runner:
    def __init__(self):
        self.running = True
        pyenergy.connect()
        pyenergy.trigger("PA0")
        gdb.execute('set pagination off')
        with Pyro4.Daemon() as self.daemon:
            print("Starting")
            pyro_uri = self.daemon.register(self)
            ns = Pyro4.locateNS()
            ns.register("runners.arm", pyro_uri)
            self.daemon.requestLoop(loopCondition=lambda: self.running)
            #daemon.serveSimple({ self : "runners.arm" }, ns=True)
            print("Stopping")

    def run_binary(self, binary_name, run):
        gdb.execute("arm_run_program {}".format(binary_name))
        gdb.execute("continue")
        returned = gdb.parse_and_eval('a')
        returned.fetch_lazy()
        gdb.execute('kill inferior 1')
        gdb.execute('delete')
        gdb.execute('monitor reset halt')
        #return (run, self.__parse_results_file(), int(returned))
        return results.Results(run, self.__parse_results_file(), int(returned))

    @staticmethod
    def __parse_results_file():
        result_ary = []
        with open('output_results', 'r') as out_file:
            for line in out_file.readlines():
                split_line = line.split(' ')
                try:
                    result_ary.append((int(split_line[1]), float(split_line[0])))
                except IndexError:
# pyenergy probably didn't finish writing the file
                    break
        return result_ary

    def ping(self):
        #TODO: Check we can run a test program
        return True

    def stop(self):
        self.running = False

class Arm_Run(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, "arm_run_program", gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL, True)

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        if len(argv) == 0:
            print("Usage: arm_run_program <program_name> [<list_of_breaks>]")
            raise BaseException

        gdb.execute('target extended :4242')
        gdb.execute('file {}'.format(argv[0]))
        gdb.execute('monitor reset halt')
        try:
            gdb.execute('load')
        except gdb.error:
    #We can't always flash first time, so try again
            gdb.execute('load')

        """breaks = []
        for i in range(1, len(argv)):
            breaks.append(argv[i])
        breaks.append("exit")

        for line in breaks:
            gdb.execute('break {}'.format(str(line)))"""
        gdb.execute('break exit')

class Arm_Quit(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, "arm_quit_program", gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL, True)

    def invoke(self, arg, from_tty):
        to_return = gdb.parse_and_eval('a')
        to_return.fetch_lazy()
        gdb.execute('kill inferior 1')
        gdb.execute('quit {}'.format(str(to_return)))

def main():
    runner = Arm_Gdb_Runner()

Arm_Run()
Arm_Quit()
if __name__ == '__main__':
    main()
