import math


class ExperimentResult:
    def __init__(self):
        self.experiment_data_results = {}

    def add_experiment_iter(self, experiment_iter_key, result_version, experiment_data):
        self.experiment_data_results[experiment_iter_key] = {
            'result_version': result_version,
            'experiment_data': experiment_data
        }

    def print_full_information(self):
        for key, value in self.experiment_data_results.items():
            print(f"№{key} - {value['result_version']}")

    def __str__(self):
        result_string = ''
        results = {}
        total = len(self.experiment_data_results)
        for key, value in self.experiment_data_results.items():
            result_version = value['result_version']
            if results.get(result_version) is None:
                results[result_version] = 0
            results[result_version] += 1

        for key, value in results.items():
            result_string += f'{key} - selected in {value} iterations ({math.floor(value / total * 100)}%)\n'
        return result_string
