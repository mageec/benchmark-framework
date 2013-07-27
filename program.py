class Program(object):
    def __init__(self, name, archs):
        self.name = name
        self.archs = archs

    def run_tests(self, logger):
        for arch in self.archs:
            arch.run_tests(self.name, logger)
