class Module:
    def __init__(self, module_id, name, versions_count):
        """
        Initialize a Module object with the given module ID, name, and number of versions.

        :param module_id: The ID of the module.
        :param name: The name of the module.
        :param versions_count: The number of versions in the module.
        """
        self.module_id = module_id
        self.name = name
        self.versions_count = versions_count

    def __str__(self):
        """
        Return a string representation of the Module object.

        :return: A string in the format "№{module_id} {name} - {versions_count} versions".
        """
        return f"№{self.module_id} {self.name} - {self.versions_count} versions"
