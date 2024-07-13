from models.module import Module


class ModuleRepository:
    def __init__(self, database):
        """
        Initialize a ModuleRepository object.

        :param database: The database connection to use for retrieving module data.
        """
        self.database = database

    def get_all_modules(self):
        """
        Retrieve all modules from the database.

        :return: A list of Module objects, each representing a module and its version count.
        """
        self.database.connect()
        modules = []
        try:
            query = """
                SELECT 
                    m.id, 
                    m.name,
                    COUNT(v.id) as versions_count 
                FROM 
                    module m 
                    INNER JOIN version v ON v.module = m.id 
                GROUP BY m.id, m.name;
            """
            cursor = self.database.execute_query(query)

            for row in cursor.fetchall():
                module = Module(module_id=row[0], name=row[1], versions_count=row[2])
                modules.append(module)
        finally:
            self.database.close()
        return modules

    def get_module(self, module_id):
        """
        Retrieve a specific module by its ID.

        :param module_id: The ID of the module to retrieve.
        :return: A Module object representing the retrieved module, or None if not found.
        """
        self.database.connect()
        try:
            query = """
                SELECT 
                    m.id, 
                    m.name,
                    COUNT(v.id) as versions_count 
                FROM 
                    module m 
                    INNER JOIN version v ON v.module = m.id 
                WHERE
                    m.id = ?
                GROUP BY m.id, m.name;
            """
            cursor = self.database.execute_query(query, (module_id,))
            row = cursor.fetchone()
        finally:
            self.database.close()
        if row:
            return Module(module_id=row[0], name=row[1], versions_count=row[2])
        return None
