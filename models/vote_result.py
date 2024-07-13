class VoteResult:
    def __init__(self):
        """
        Initialize a VoteResult object.

        This class is used to store and manage the results of voting on experiment data.
        """
        self.vote_data_results = {}

    def add_experiment_iter(self, experiment_iter_key, result_version, result_value, correct_answer, experiment_data):
        """
        Add an iteration of experiment results to the vote data.

        :param experiment_iter_key: The key identifying the experiment iteration.
        :param result_version: The version name of the result.
        :param result_value: The value of the result.
        :param correct_answer: The correct answer for the experiment.
        :param experiment_data: The data of the experiment.
        """
        self.vote_data_results[experiment_iter_key] = {
            'result_version': result_version,
            'result_value': result_value,
            'correct_answer': correct_answer,
            'experiment_data': experiment_data
        }

    def print_full_information(self):
        """
        Print full information of all experiment results stored in the vote data.
        """
        for key, value in self.vote_data_results.items():
            print(f"№{key} - {value['result_version']}")

    def __str__(self):
        """
        Return a string representation of the VoteResult object.

        The string includes information about the frequency of each result version across all experiment iterations.

        :return: A string summarizing the vote results.
        """
        result_string = ''
        results = {}
        total = len(self.vote_data_results)
        for key, value in self.vote_data_results.items():
            result_version = value['result_version']
            if results.get(result_version) is None:
                results[result_version] = 0
            results[result_version] += 1

        for key, value in results.items():
            result_string += f'{key} - selected in {value} iterations ({round(value / total * 100, 1)}%)\n'
        return result_string
