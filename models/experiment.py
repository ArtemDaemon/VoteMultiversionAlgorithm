class Experiment:
    def __init__(self, experiment_id, name, iterations_count):
        self.experiment_id = experiment_id
        self.name = name
        self.iterations_count = iterations_count
        self.experiments_data = None

    def __str__(self):
        return f'№ {self.experiment_id} {self.name} - {self.iterations_count} iterations'
