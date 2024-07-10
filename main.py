import math

from database import Database
from models.vote_result import VoteResult
from repos.vote_result_repository import VoteResultRepository
from repos.module_repository import ModuleRepository
from repos.experiment_repository import ExperimentRepository

menu_dict = {
    'Choose module': 1,
    'Choose experiment': 2,
    'Vote experiment data': 3,
    'Show full vote result': 4,
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
        chosen_experiment = experiments[choice - 1]
        chosen_experiment.experiments_data = repository.get_experiment_data_by_name(chosen_experiment.name)
        return chosen_experiment
    return None


def check_multiple_seq_counter(equal_seq_counter, t):
    first_length = equal_seq_counter[0]['length']
    if first_length < t:
        return False
    for i in range(1, len(equal_seq_counter)):
        if equal_seq_counter[i]['length'] != first_length:
            return False
    return True


def get_result_index(t, n, output_versions, equal_seq_counter):
    if len(equal_seq_counter) == 1 and equal_seq_counter[0]['length'] >= t:
        for i in range(equal_seq_counter[0]['start'],
                       equal_seq_counter[0]['start'] + equal_seq_counter[0]['length'] + 1):
            if i in output_versions:
                return i
    if (len(equal_seq_counter) == 1 and equal_seq_counter[0]['length'] < t) or (
            len(equal_seq_counter) > 1 and check_multiple_seq_counter(equal_seq_counter, t)):
        return n - 1
    return None


def vote_experiment_data(experiment):
    result = VoteResult()

    sample_key = next(iter(experiment.experiments_data))
    n = len(experiment.experiments_data[sample_key])
    t = math.floor((n - 1) / 2)
    step = math.ceil((n - 1) / (n - t - 1))
    output_versions = []

    for i in range(0, n - 2, step):
        output_versions.append(i)

    output_versions.append(n - 1)

    for key, value in experiment.experiments_data.items():
        equal_seq_counter = []
        is_last_compare_equal = False

        for i in range(n - 1):
            if value[i].version_answer == value[i + 1].version_answer:
                if is_last_compare_equal:
                    equal_seq_counter[len(equal_seq_counter) - 1]['length'] += 1
                else:
                    equal_seq_counter.append({
                        'start': i,
                        'length': 2
                    })
                    is_last_compare_equal = True
            else:
                is_last_compare_equal = False

        result_index = get_result_index(t, n, output_versions, equal_seq_counter)
        if result_index is None and value[n - 2].version_answer == value[n - 1].version_answer:
            if is_last_compare_equal:
                equal_seq_counter[len(equal_seq_counter) - 1]['length'] += 1
            else:
                equal_seq_counter.append({
                    'start': n - 2,
                    'length': 2
                })
            result_index = get_result_index(t, n, output_versions, equal_seq_counter)

        if result_index is None:
            result.add_experiment_iter(key, None, None, value)
        else:
            result.add_experiment_iter(key, value[result_index].version_name, value[result_index].version_answer, value)

    return result


def save_vote_results(repository, module, experiment, vote_results):
    repository.save_vote_results(module.name, experiment.name, vote_results)
    print('Vote results loaded to DB')


def main():
    db = Database("experiment_edu.db")
    module_repository = ModuleRepository(db)
    experiment_repository = ExperimentRepository(db)
    vote_result_repository = VoteResultRepository(db)

    current_module = None
    current_experiment = None
    current_vote_results = None

    user_input = None
    while user_input != menu_dict['Exit']:
        print('\n')
        print(f'Current module: {str(current_module)}')
        print(f'Current experiment: {str(current_experiment)}')
        print(f'Current results: \n{str(current_vote_results)}')
        print('\n')
        display_menu()

        user_input = get_valid_int("Please choose menu item: ")

        if user_input == menu_dict['Choose module']:
            current_module = select_module(module_repository)
            current_experiment = None
            current_vote_results = None
        elif user_input == menu_dict['Choose experiment']:
            if current_module is None:
                print('You should choose module first')
                continue
            current_experiment = select_experiment(experiment_repository, current_module)
            current_vote_results = None
        elif user_input == menu_dict['Vote experiment data']:
            if current_experiment is None:
                print('You should choose experiment first')
                continue
            current_vote_results = vote_experiment_data(current_experiment)
            save_vote_results(vote_result_repository, current_module, current_experiment,
                              current_vote_results)
        elif user_input == menu_dict['Show full vote result']:
            if current_vote_results is None:
                print('You should choose Vote menu item first')
                continue
            current_vote_results.print_full_information()
        elif user_input == menu_dict['Exit']:
            print('Goodbye!')
        else:
            print('You enter an incorrect input!')


if __name__ == "__main__":
    main()

# Выводить данные своего алгоритма
# Сравнить данные по каждому модулю и итерации
# Проверить код
# Написать док комменты
# Написать комментарии для каждой строчки алгоритма
