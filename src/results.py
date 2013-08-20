class Results:
    def __init__(self, run, results=[], return_code=None):
        self.run = run
        self.results = results
        self.return_code = return_code

    def record_result(self, time, energy):
        if not type(time) is int:
            raise AttributeError("time")
        self.results.append((time, energy))

    def __str__(self):
        to_return = str(self.run)
        to_return += "\n"
        to_return += "Results:\n"
        for result in self.results:
            to_return += str(result)
            to_return += "\n"
        return to_return
