from database import Database
from repos.module_repository import ModuleRepository


def main():
    db = Database("experiment_edu.db")
    module_repository = ModuleRepository(db)
    modules = module_repository.get_all_modules()
    for module in modules:
        print(module)

    # TODO: Выбрать модуль
    # TODO: Выбрать эксперимент
    # TODO: Провести эксперимент


if __name__ == "__main__":
    main()
