class Results:
    def __init__(self, program, arch, test):
        self.program = program
        self.arch = arch
        self.test = test
        self.results = []
        self.passed = True

    def append(self, result):
        self.results.append(result)

    def fail(self):
        self.passed = False

    def __add__(self, other):
        sum(self.results) + other

    def __radd__(self, other):
        sum(self.results) + other

    def __iter__(self):
        return self.results.__iter__()

    def __len__(self):
        return self.results.__len__()

    def __str__(self):
        to_return  = "*** {} results for {} ***".format(str(arch), str(program))
        for result in self.results:
            if not result.passed:
                to_return += "\n{}".format(result.error)
                break # Only log the first result, assume the rest are the same
            else:
                to_return += "\n{}".format(str(result))

        return to_return
