class ExperimentResultRepository:
    def __init__(self, database):
        self.database = database

    def save_experiment_results(self, module_name, version_name, ):