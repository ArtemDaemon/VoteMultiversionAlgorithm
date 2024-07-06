from models.module import Module


class ModuleRepository:
    def __init__(self, database):
        self.database = database

    def get_all_modules(self):
        self.database.connect()
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
        modules = []

        for row in cursor.fetchall():
            module = Module(module_id=row[0], name=row[1], versions_count=row[2])
            modules.append(module)

        self.database.close()
        return modules

    def get_module(self, module_id):
        self.database.connect()
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
        self.database.close()
        if row:
            return Module(module_id=row[0], name=row[1], versions_count=row[2])
        return None
