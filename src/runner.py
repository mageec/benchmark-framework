class Runner:
    def __init__(self, logger, gdb_manager):
        self.logger = logger
        self.gdb_manager = gdb_manager

    def run_binary(self, binary_name, run):
        return self.gdb_manager.read_energy(binary_name, run)
