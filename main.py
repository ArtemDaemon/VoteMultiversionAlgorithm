from database import Database
from repos.module_repository import ModuleRepository

menu_dict = {
    'Choose module': 1,
    'Exit': 0
}


def display_menu():
    for key, value in menu_dict.items():
        print(f'{value} - {key}')


def get_valid_int(min_value, max_value):
    is_input_valid = False
    user_input = None
    while not is_input_valid:
        try:
            user_input = int(input("Please enter: "))
            if user_input < min_value or user_input > max_value:
                raise ValueError(f'Expected value from {min_value} to {max_value}')
        except ValueError as err:
            print('Entered value is incorrect! ' + str(err))
        except Exception as err:
            print('Unknown error! ' + str(err))
        else:
            is_input_valid = True
    return user_input


def main():
    db = Database("experiment_edu.db")
    module_repository = ModuleRepository(db)

    current_module = None

    user_input = None
    while user_input != menu_dict['Exit']:
        print(f'Current module: {str(current_module)}\n')
        display_menu()

        user_input = get_valid_int(0, len(menu_dict.items()) - 1)

        if user_input == menu_dict['Choose module']:
            print('hello')
        else:
            print('goodbye')

    # TODO: Выбрать модуль
    # TODO: Выбрать эксперимент
    # TODO: Провести эксперимент


if __name__ == "__main__":
    main()
