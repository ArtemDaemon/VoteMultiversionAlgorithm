import math

from database import Database
from models.experiment_result import ExperimentResult
from repos.module_repository import ModuleRepository
from repos.experiment_repository import ExperimentRepository

menu_dict = {
    'Choose module': 1,
    'Choose experiment': 2,
    'Vote experiment data': 3,
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
    for index, experiment in enumerate(experiments):
        print(f'№{index + 1} {experiment}')

    choice = get_valid_int("Please choose experiment: ")
    if 0 < choice < len(experiments):
        chosen_experiment = experiments[choice]
        chosen_experiment.experiments_data = repository.get_experiment_data_by_name(chosen_experiment.name)
        return chosen_experiment
    return None


def vote_experiment_data(experiment):
    sample_key = next(iter(experiment.experiment_data))
    n = len(experiment.experiment_data[sample_key])
    t = math.floor((n - 1) / 2)
    step = math.ceil((n - 1) / (n - t - 1))

    for key, value in experiment.experiment_data.items():
        output_versions = []

        for i in range(0, n - 2, step):
            output_versions.append(value[i])

        output_versions.append(value[-1])

        equal_seq_counter = {}

        for i in range(n - 2):
            if value[i].version_answer == value[i + 1].version_answer:
                if


def main():
    db = Database("experiment_edu.db")
    module_repository = ModuleRepository(db)
    experiment_repository = ExperimentRepository(db)

    current_module = None
    current_experiment = None
    current_experiment_results = None

    user_input = None
    while user_input != menu_dict['Exit']:
        print('\n')
        print(f'Current module: {str(current_module)}')
        print(f'Current experiment: {str(current_experiment)}')
        print(f'Current results: {str(current_experiment_results)}')
        print('\n')
        display_menu()

        user_input = get_valid_int("Please choose menu item: ")

        if user_input == menu_dict['Choose module']:
            current_module = select_module(module_repository)
            current_experiment = None
            current_experiment_results = None
        elif user_input == menu_dict['Choose experiment']:
            if current_module is None:
                print('You should choose module first')
                continue
            current_experiment = select_experiment(experiment_repository, current_module)
            current_experiment_results = None
        elif user_input == menu_dict['Vote experiment data']:
            if current_experiment is None:
                print('You should choose experiment first')
                continue
            current_experiment_results = vote_experiment_data(current_experiment)
        elif user_input == menu_dict['Exit']:
            # TODO: Написать прощание
            print('goodbye')
        else:
            print('You enter an incorrect input!')

    # TODO: Провести эксперимент


if __name__ == "__main__":
    main()
