class Experiment:
    def __init__(self, name, iterations_count):
        self.name = name
        self.iterations_count = iterations_count
        self.experiments_data = None

    def __str__(self):
        return f'{self.name} - {self.iterations_count} iterations'
