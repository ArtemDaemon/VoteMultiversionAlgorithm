import sqlite3


class Database:
    def __init__(self, db_name):
        """
        Initialize the Database object with the given database name.

        :param db_name: The name of the database file.
        """
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """
        Establish a connection to the SQLite database.
        """
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        """
        Close the connection to the SQLite database.
        """
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=()):
        """
        Execute a single SQL query with optional parameters.

        :param query: The SQL query to execute.
        :param params: A tuple of parameters to substitute into the query.
        :return: The cursor object after executing the query.
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def execute_many(self, query, params):
        """
        Execute a batch of SQL queries with the given parameters.

        :param query: The SQL query to execute.
        :param params: A list of tuples, each containing parameters for the query.
        :return: The cursor object after executing the queries.
        """
        cursor = self.connection.cursor()
        cursor.executemany(query, params)
        self.connection.commit()
        return cursor
