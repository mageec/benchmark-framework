class Result:
    def __init__(self, passed, result="", error=""):
        self.passed = passed
        self.result = result
        self.error = error

    def __add__(self, other):
        return self.result + other

    def __radd__(self, other):
        return self.result + other

    def __str__(self):
        if self.passed:
            return str(self.result)
        else:
            return "Fail: {}".format(self.error)
