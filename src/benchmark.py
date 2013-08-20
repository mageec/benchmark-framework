class Benchmark:
    def __init__(self, name, build_flags):
        self.name = name
        self.build_flags = build_flags

    def build_flags_for(self, compiler):
        try :
            return self.build_flags[compiler]
        except KeyError:
            return None

    def __str__(self):
        return self.name
