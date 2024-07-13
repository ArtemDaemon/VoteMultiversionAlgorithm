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
    'Run vote analysis': 5,
    'Exit': 0
}


def display_menu():
    """
    Display the menu options to the user.
    """
    for option, value in menu_dict.items():
        print(f'{value} - {option}')


def get_valid_int(user_str):
    """
    Prompt the user for an integer input and validate the input.

    :param user_str: The prompt string to display to the user.
    :return: The valid integer input from the user.
    """
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
    """
    Display available modules and prompt the user to select one.

    :param repository: The repository to fetch modules from.
    :return: The selected module object, or None if no modules are found or selection is invalid.
    """
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
    """
    Display available experiments for the selected module and prompt the user to select one.

    :param repository: The repository to fetch experiments from.
    :param module: The module for which to fetch experiments.
    :return: The selected experiment object, or None if no experiments are found or selection is invalid.
    """
    print('It will take some time...')
    experiments = repository.get_all_experiments(module.module_id)
    if not experiments:
        print('No experiments found.')
        return None
    print('Available experiments:')
    for index, experiment in enumerate(experiments):
        print(f'№{index + 1} {experiment}')

    choice = get_valid_int("Please choose experiment: ")
    if 0 < choice <= len(experiments):
        chosen_experiment = experiments[choice - 1]
        chosen_experiment.experiments_data = repository.get_experiment_data_by_name(chosen_experiment.name)
        return chosen_experiment
    return None


def get_result_index(t, output_versions, equal_seq_counter):
    """
    Determine the index of the result based on the given parameters.

    :param t: Number of untrusted versions.
    :param output_versions: The list of output version indices.
    :param equal_seq_counter: The list of equal sequence counters.
    :return: The index of the result, or None if no suitable result is found.
    """
    # An array of sequences longer than t
    greater_than_t = []
    # An array of sequences equal t
    equal_t = []
    # An array of sequences less than t
    less_than_t = []

    # We parse sequences into arrays based on their length
    for equal_seq in equal_seq_counter:
        if equal_seq['length'] > t:
            greater_than_t.append(equal_seq)
            continue
        if equal_seq['length'] == t:
            equal_t.append(equal_seq)
            continue
        less_than_t.append(equal_seq)

    # If there is only one sequence of length greater than t or only one sequence of length equal to t
    if len(greater_than_t) == 1 or len(equal_t) == 1:
        # The first output version in this sequence is sent to the module output
        chosen_array = greater_than_t if len(greater_than_t) == 1 else equal_t
        for i in range(chosen_array[0]['start'],
                       chosen_array[0]['start'] + chosen_array[0]['length']):
            if i in output_versions:
                return i

    # If there is only one sequence with length less than t or several sequences with length greater than or equal to t
    if len(less_than_t) == 1 or (len(greater_than_t) + len(equal_t)) > 1:
        # The last version which was not compared is returned.
        return output_versions[-1]

    # In any other case, it is impossible to obtain the index of the correct version
    return None


def vote_experiment_data(experiment):
    """
    Perform voting on the experiment data to determine the result.

    :param experiment: The experiment object containing the data to vote on.
    :return: A VoteResult object containing the voting results.
    """
    result = VoteResult()

    # Since all iterations of one experiment contain the same number of versions,
    # we take the first iteration to initialize the base variables
    sample_key = next(iter(experiment.experiments_data))
    # Number of versions
    n = len(experiment.experiments_data[sample_key])
    # Number of untrusted versions
    t = math.floor((n - 1) / 2)
    # Step for calculating version indices whose values can be output
    step = math.ceil((n - 1) / (n - t - 1))
    # Indexes of versions whose values can be output
    # Includes the first, latest versions and all versions by the above step
    output_versions = list(range(0, n - 1, step))
    output_versions.append(n - 1)

    # Loop through all iterations of the experiment
    for key, value in experiment.experiments_data.items():
        # An array for storing sequences of consecutive identical values.
        # Will store dictionaries:
        # start - the index from which the sequence began (from 0 to n -1),
        # length - the number of consecutive versions with the same values (from 1 to n)
        equal_seq_counter = []
        # A label to indicate whether the values of a previous pair of versions are the same
        is_last_compare_equal = False

        # Pairwise comparison of every two versions except the last one
        for i in range(n - 2):
            # If the version value is the same as the next version value
            if value[i].version_answer == value[i + 1].version_answer:
                # If previous versions also had the same values,
                # increase the length of the last sequence in the array by 1
                if is_last_compare_equal:
                    equal_seq_counter[-1]['length'] += 1
                # Otherwise, adds a new sequence of two consecutive versions and puts a mark for the next comparison
                else:
                    equal_seq_counter.append({
                        'start': i,
                        'length': 2
                    })
                    is_last_compare_equal = True
            # Otherwise, if the current element does not participate in the sequence of consecutive versions
            # with the same values, we add a sequence one version long.
            # In any case, we put a mark for the following comparisons
            else:
                if is_last_compare_equal:
                    is_last_compare_equal = False
                else:
                    equal_seq_counter.append({
                        'start': i,
                        'length': 1
                    })

        # We get the version index, the value of which will be output to the module, or None
        result_index = get_result_index(t, output_versions, equal_seq_counter)
        # If the version index was not obtained
        # and the values of the last two versions that were not previously compared are equal
        if result_index is None and value[n - 2].version_answer == value[n - 1].version_answer:
            # We add a new sequence, or increase the length of the last one
            if is_last_compare_equal:
                equal_seq_counter[-1]['length'] += 1
            else:
                equal_seq_counter.append({
                    'start': n - 2,
                    'length': 2
                })
            # and again try to get the index of the output version
            result_index = get_result_index(t, output_versions, equal_seq_counter)

        # The value that should be obtained as a result of the experiment iteration
        correct_answer = value[0].correct_answer
        if result_index is None:
            result.add_experiment_iter(key, None, None, correct_answer, value)
        else:
            result.add_experiment_iter(key, value[result_index].version_name, value[result_index].version_answer,
                                       correct_answer, value)

    return result


def save_vote_results(repository, module, experiment, vote_results):
    """
    Save the voting results to the database.

    :param repository: The VoteResultRepository to interact with the database.
    :param module: The module object.
    :param experiment: The experiment object.
    :param vote_results: The VoteResult object containing the voting results.
    """
    repository.delete_vote_results(module.name, experiment.name)
    repository.save_vote_results(module.name, experiment.name, vote_results)
    print('Vote results loaded to DB')


def run_vote_analysis(vote_results):
    """
    Perform analysis on the voting results and print the analysis.

    :param vote_results: The VoteResult object containing the voting results.
    """
    total = len(vote_results.vote_data_results)
    correct_counter = 0
    none_counter = 0
    failed_counter = 0
    for key, value in vote_results.vote_data_results.items():
        if value['result_value'] == value['correct_answer']:
            correct_counter += 1
            continue
        if value['result_value'] is None:
            none_counter += 1
            continue
        failed_counter += 1

    print('Vote analysis:')
    print(f'The algorithm find correct answer in {correct_counter} experiment iterations '
          f'({round(correct_counter / total * 100, 1)}%)')
    print(f'The algorithm find wrong answer in {failed_counter} experiment iterations '
          f'({round(failed_counter / total * 100, 1)}%)')
    print(f"The algorithm could not find any answer in {none_counter} experiment iterations "
          f'({round(none_counter / total * 100, 1)}%)')


def main():
    """
    Main function to run the application. Initializes repositories and handles user input to interact with the system.
    """
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
        elif user_input == menu_dict['Run vote analysis']:
            if current_vote_results is None:
                print('You should choose Vote menu item first')
                continue
            run_vote_analysis(current_vote_results)
        elif user_input == menu_dict['Exit']:
            print('Goodbye!')
        else:
            print('You enter an incorrect input!')


if __name__ == "__main__":
    main()

# Write doc comments
# Comment each row of algorithm
