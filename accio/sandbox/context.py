class Context:
    def __init__(self):
        self.filename = ""
        self.ignore = False
        self.variables = {}

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        return self.variables[name]