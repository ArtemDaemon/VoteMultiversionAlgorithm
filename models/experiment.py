class Experiment:
    def __init__(self, name, iterations_count):
        """
        Initialize an Experiment object with the given name and number of iterations.

        :param name: The name of the experiment.
        :param iterations_count: The number of iterations in the experiment.
        """
        self.name = name
        self.iterations_count = iterations_count
        self.experiments_data = None

    def __str__(self):
        """
        Return a string representation of the Experiment object.

        :return: A string that represents the experiment's name and the number of iterations.
        """
        return f'{self.name} - {self.iterations_count} iterations'
