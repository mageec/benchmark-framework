class Run:
    def __init__(self, benchmark, compiler, platform, flags, id):
        self.benchmark = benchmark
        self.compiler = compiler
        self.platform = platform
        self.flags = flags
        self.id = id

    def __str__(self):
        return "Run id: {}".format(self.id)
