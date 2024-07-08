from models.experiment import Experiment


class ExperimentRepository:
    def __init__(self, database):
        self.database = database

    def get_all_experiments(self, module_id):
        self.database.connect()
        query = """
            SELECT
                row_number() OVER () AS experiment_id,
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
            experiment = Experiment(experiment_id=row[0], name=row[1], iterations_count=row[2])
            experiments.append(experiment)

        self.database.close()
        return experiments
