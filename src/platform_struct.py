class Platform:
    def __init__(self, name, compilers, build_flags, runner_name):
        self.name = name
        self.compilers = compilers
        self.build_flags = build_flags
        self.runner_name = runner_name

    def compiler_bin_for(self, compiler):
        try:
            return self.compilers[compiler]
        except KeyError:
            return None

    def build_flags_for(self, compiler):
        try:
            return self.build_flags[compiler]
        except KeyError:
            return None

    def __str__(self):
        return self.name
