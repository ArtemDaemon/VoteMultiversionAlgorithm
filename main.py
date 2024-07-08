from database import Database
from repos.module_repository import ModuleRepository
from repos.experiment_repository import ExperimentRepository

menu_dict = {
    'Choose module': 1,
    'Choose experiment': 2,
    'Exit': 0
}


def display_menu():
    for key, value in menu_dict.items():
        print(f'{value} - {key}')


def get_valid_int(user_str):
    is_input_valid = False
    user_input = None
    while not is_input_valid:
        try:
            user_input = int(input(user_str))
            is_input_valid = True
        except ValueError as err:
            print('Entered value is incorrect! ' + str(err))
        except Exception as err:
            print('Unknown error! ' + str(err))
    return user_input


def select_module(repository):
    modules = repository.get_all_modules()
    if not modules:
        print('No modules found.')
        return None
    print('Available modules:')
    for module in modules:
        print(module)

    choice = get_valid_int("Please choose module: ")
    return repository.get_module(choice)


def select_experiment(repository, module):
    print('It will take some time...')
    experiments = repository.get_all_experiments(module.module_id)
    if not experiments:
        print('No experiments found.')
        return None
    print('Available experiments:')
    for experiment in experiments:
        print(experiment)

    # choice = get_valid_int("Please choose experiment: ")
    #
    # return repository.get_module(choice)


def main():
    db = Database("experiment_edu.db")
    module_repository = ModuleRepository(db)
    experiment_repository = ExperimentRepository(db)

    current_module = None
    current_experiment = None

    user_input = None
    while user_input != menu_dict['Exit']:
        print('\n')
        print(f'Current module: {str(current_module)}')
        print(f'Current experiment: {str(current_experiment)}')
        print('\n')
        display_menu()

        user_input = get_valid_int("Please choose menu item: ")

        if user_input == menu_dict['Choose module']:
            current_module = select_module(module_repository)
            current_experiment = None
        elif user_input == menu_dict['Choose experiment']:
            if current_module is None:
                print('You should choose module first')
                continue
            current_experiment = select_experiment(experiment_repository, current_module)
        elif user_input == menu_dict['Exit']:
            # TODO: Написать прощание
            print('goodbye')
        else:
            print('You enter an incorrect input!')

    # TODO: Выбрать эксперимент
    # TODO: Провести эксперимент


if __name__ == "__main__":
    main()
