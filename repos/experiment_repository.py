from models.experiment import Experiment


class ExperimentRepository:
    def __init__(self, database):
        self.database = database

    def get_all_experiments(self, module_id):
        self.database.connect()
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
        experiments = []

        for row in cursor.fetchall():
            experiment = Experiment(name=row[0], iterations_count=row[1])
            experiments.append(experiment)

        self.database.close()
        return experiments

    def get_experiment_data_by_name(self, experiment_name):
        self.database.connect()
        query = """
            SELECT
                experiment_name,
                COUNT(DISTINCT module_iteration_num) as iterations_count
            FROM
                experiment_data
            WHERE
                experiment_name = ?
            GROUP BY
                experiment_name
            ORDER BY
                iterations_count;
        """
        cursor = self.database.execute_query(query, (experiment_name,))
        row = cursor.fetchone()
        self.database.close()
        if row:
            return Experiment(experiment_id=row[0], name=row[1], iterations_count=row[2])
        return None