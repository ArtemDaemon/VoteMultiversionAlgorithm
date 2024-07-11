class VoteResult:
    def __init__(self):
        self.vote_data_results = {}

    def add_experiment_iter(self, experiment_iter_key, result_version, result_value, correct_answer, experiment_data):
        self.vote_data_results[experiment_iter_key] = {
            'result_version': result_version,
            'result_value': result_value,
            'correct_answer': correct_answer,
            'experiment_data': experiment_data
        }

    def print_full_information(self):
        for key, value in self.vote_data_results.items():
            print(f"№{key} - {value['result_version']}")

    def __str__(self):
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
