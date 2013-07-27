class Arm_Run(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, "arm_run_program", gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL, True)

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        if len(argv) == 0:
            print "Usage: arm_run_program <program_name> [<list_of_breaks>]"
            raise BaseException

        gdb.execute('target extended :4242')
        gdb.execute('file arm_{}'.format(argv[0]))
        gdb.execute('monitor reset halt')
        try:
            gdb.execute('load')
        except gdb.error:
    #We can't always flash first time, so try again
            gdb.execute('load')

        breaks = []
        for i in range(1, len(argv)):
            breaks.append(argv[i])
        breaks.append("exit")

        for line in breaks:
            gdb.execute('break {}'.format(str(line)))

        gdb.execute('continue')

class Arm_Quit(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, "arm_quit_program", gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL, True)

    def invoke(self, arg, from_tty):
        to_return = gdb.parse_and_eval('a')
        to_return.fetch_lazy()
        gdb.execute('kill inferior 1')
        gdb.execute('quit {}'.format(str(to_return)))

Arm_Run()
Arm_Quit()
