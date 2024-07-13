from models.experiment import Experiment
from models.experiment_data import ExperimentData


class ExperimentRepository:
    def __init__(self, database):
        """
        Initialize an ExperimentRepository object.

        :param database: The database connection to use for retrieving experiment data.
        """
        self.database = database

    def get_all_experiments(self, module_id):
        """
        Retrieve all experiments associated with a given module.

        :param module_id: The ID of the module whose experiments are to be retrieved.
        :return: A list of Experiment objects, each representing an experiment and its iteration count.
        """
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
        """
        Retrieve data for a specific experiment by its name.

        :param experiment_name: The name of the experiment whose data is to be retrieved.
        :return: A dictionary where keys are iteration numbers and values are lists of ExperimentData objects.
        """
        self.database.connect()
        experiment_data = {}
        try:
            query = """
                SELECT
                    version_name,
                    version_answer,
                    correct_answer,
                    module_iteration_num
                FROM
                    experiment_data
                WHERE
                    experiment_name = ?;
            """
            cursor = self.database.execute_query(query, (experiment_name,))
            for row in cursor.fetchall():
                new_experiment_data = ExperimentData(version_name=row[0], version_answer=row[1], correct_answer=row[2])
                experiment_data.setdefault(row[3], []).append(new_experiment_data)
        finally:
            self.database.close()
        return experiment_data
