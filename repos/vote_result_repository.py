class VoteResultRepository:
    def __init__(self, database):
        """
        Initialize a VoteResultRepository object.

        :param database: The database connection to use for vote result operations.
        """
        self.database = database

    def save_vote_results(self, module_name, experiment_name, vote_results):
        """
        Save vote results to the database.

        :param module_name: The name of the module associated with the vote results.
        :param experiment_name: The name of the experiment associated with the vote results.
        :param vote_results: The VoteResult object containing the results to be saved.
        """
        self.database.connect()
        try:
            query = """
                        INSERT INTO
                            vote_result_2
                            (module, experiment, iter, result)
                        VALUES (?,?,?,?);
                    """
            params = [
                (module_name, experiment_name, key, value['result_value'])
                for key, value in vote_results.vote_data_results.items()
            ]
            self.database.execute_many(query, params)
        finally:
            self.database.close()

    def delete_vote_results(self, module_name, experiment_name):
        """
        Delete vote results from the database for a specific module and experiment.

        :param module_name: The name of the module whose vote results are to be deleted.
        :param experiment_name: The name of the experiment whose vote results are to be deleted.
        """
        self.database.connect()
        try:
            query = """
                        DELETE
                        FROM
                            vote_result_2
                        WHERE
                            module = ?
                            AND experiment = ?
                    """
            self.database.execute_query(query, (module_name, experiment_name,))
        finally:
            self.database.close()

    def create_table(self):
        """
        Create the vote_result_2 table in the database if it does not already exist.
        """
        self.database.connect()
        try:
            query = """
                        CREATE TABLE IF NOT EXISTS "vote_result_2" (
                            "module"	TEXT,
                            "experiment"	TEXT,
                            "iter"	INTEGER,
                            "result"	REAL
                            )
                    """
            self.database.execute_query(query)
        finally:
            self.database.close()
