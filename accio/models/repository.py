class Repository:
    def __init__(self, url: str, directory: str):
        self.url = url
        self.generators = {}
        self.directory = directory

    def add_generator(self, generator):
        self.generators[generator.name] = generator
