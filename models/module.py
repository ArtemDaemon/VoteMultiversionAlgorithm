class Module:
    def __init__(self, module_id, name, versions_count):
        self.module_id = module_id
        self.name = name
        self.versions_count = versions_count

    def __str__(self):
        return f"№{self.module_id} {self.name} - {self.versions_count} versions"
