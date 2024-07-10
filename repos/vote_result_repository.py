class VoteResultRepository:
    def __init__(self, database):
        self.database = database

    def save_vote_results(self, module_name, experiment_name, vote_results):
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
