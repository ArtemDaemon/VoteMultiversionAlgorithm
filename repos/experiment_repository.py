from models.experiment import Experiment
from models.experiment_data import ExperimentData


class ExperimentRepository:
    def __init__(self, database):
        self.database = database

    def get_all_experiments(self, module_id):
        self.database.connect()
        experiments = []
        try:
            query = """
                SELECT
                    experiment_name,
                    COUNT(DISTINCT module_iteration_num) as iterations_count
                FROM
                    experiment_data
                WHERE
                    module_id = ?
                GROUP BY
                    experiment_name
                ORDER BY
                    iterations_count;
            """
            cursor = self.database.execute_query(query, (module_id,))

            for row in cursor.fetchall():
                experiment = Experiment(name=row[0], iterations_count=row[1])
                experiments.append(experiment)
        finally:
            self.database.close()
        return experiments

    def get_experiment_data_by_name(self, experiment_name):
        self.database.connect()
        experiment_data = {}
        try:
            query = """
                SELECT
                    version_name,
                    version_answer,
                    module_iteration_num
                FROM
                    experiment_data
                WHERE
                    experiment_name = ?;
            """
            cursor = self.database.execute_query(query, (experiment_name,))
            for row in cursor.fetchall():
                new_experiment_data = ExperimentData(version_name=row[0], version_answer=row[1])
                experiment_data.setdefault(row[3], []).append(new_experiment_data)
        finally:
            self.database.close()
        return experiment_data
