import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('yarn_genie')
patterns = SHEET.worksheet('patterns')
data = patterns.get_all_values()


# Worksheet Manipulation Section
def show_worksheet(worksheet):
    """
    Print out a table of all the values from specific worksheet
    """
    print(f'You have the following {worksheet} in your stash!\n')
    stash = SHEET.worksheet(worksheet).get_all_values()
    print(tabulate(stash))


def add_to_worksheet(data, worksheet):
    """
    Update relevant worksheet, add new row with list data provided
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully!\n')

    if worksheet == 'yarns':
        show_worksheet(worksheet)


def remove_from_worksheet(worksheet):
    print('Which item do you want to remove?\n')



# User input section
def get_user_data(type, num):
    """
    Get pattern/yarn/hook information input from user
    """
    while True:
        print(f'Please enter your {type} information.')
        print(f'\nInformation should be {num} categories, separate by commas.')

        if type == 'pattern':
            print(f'{type.capitalize()} Name, Yarn Weight, Yarn Length (m), Hook Size\n')
            print('Example: Kids Gloves, Double Knit, 400, 3.00\n')

            pattern_data = input(f'Enter your {type} information here '
                                'or enter "x" to return to sub-menu: \n')
            if pattern_data.upper() == 'X':
                print('Returning to sub-menu\n')
                show_worksheet('patterns')
                return []

            pattern_info = pattern_data.split(',')
            if validate_pattern(pattern_info):
                print('\nInformation is valid!')
                add_to_worksheet(pattern_info, 'patterns')

        elif type == 'yarn':
            print(f'{type.capitalize()} Name, Material, {type.capitalize()} Weight, {type.capitalize()} Length, Colour, Quantity\n')
            print('Example: Rico, Cotton, Double Knit, 200, Teal, 1\n')

            yarn_data = input(f'Enter your {type} information here '
                                'or enter "x" to return to sub-menu: \n')
            if yarn_data.upper() == 'X':
                print('Returning to sub-menu\n')
                show_worksheet('yarns')
                return []

            yarn_info = yarn_data.split(',')
            if validate_yarn(yarn_info):
                print('\nInformation is valid!')
                add_to_worksheet(yarn_info, 'yarns')

        elif type == 'hook':
            print(f'{type.capitalize()} Size, Owned\n')
            print('Example: 6.00, True\n')
            
            hook_data = input(f'Enter your {type} information here '
                                'or enter "x" to return to sub-menu: \n')

            if hook_data.upper() == 'X':
                print('Returning to sub-menu\n')
                show_worksheet('hooks')
                return []

            hook_info = hook_data.split(',')
            if validate_hook(hook_info):
                print('\nInformation is valid!')
                add_to_worksheet(hook_info, 'hooks')

        else:
            print('Invalid data, please try again\n')
            input('Press Enter to continue...\n')


def validate_pattern(values):
    """
    Check if the patterns input contains exactly 4 values
    """
    try:
        if len(values) != 4:
            raise ValueError(
                f'4 values required, you provided {len(values)}'    
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True

def validate_yarn(values):
    """
    Convert the 3rd and 5th index into integers.
    Raise ValueError if strings cannot be converted into integers,
    or if there aren't exactly 6 values.
    """
    try:
        # convert data at 3rd and 5th indices into intergers
        indices = [3, 5]
        for index in indices:
            values[index] = int(values[index])

        if len(values) != 6:
            raise ValueError(
                f'6 values required, you provided {len(values)}'    
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True

def validate_hook(values):
    """
    Check if user has input the correct values for hooks
    """
    try:
        # convert data at 1st to be boolean
        values[1] = bool(values[1])

        if len(values) != 2:
            raise ValueError(
                f'2 values required, you provided {len(values)}'    
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True

# Hooks Section

def sub_menu(str, add_func, remove_func):
    """
    Display add and back sub menu until the user select a valid option
    then calls the requested funcion
    
        Arguments:
            str: title of the submenu (patterns/yarns/hooks)
            add_func: calls add_function
            back_func: calls back function
    """
    while True:
        print(f'\n1. Add a {str}')
        print(f'2. Remove last added {str}')
        print(f'3. Go back to main menu')

        user_input = input('\nPlease select an option by entering a number from 1, 2, or 3\n')

        if user_input == '1':
            if str == 'pattern':
                get_user_data('pattern', 4)
            elif str == 'yarn':
                get_user_data('yarn', 6)
            elif str == 'hook':
                get_user_data('hook', 2)
        elif user_input == '2':
            remove_from_worksheet
        elif user_input == '3':
            break
        else:
            print('Invalid option, please eneter a number from 1, 2, or 3\n')
            input('Press Enter to continue...\n')


def main_menu():
    """
    Display the main menu to the user until they select an option or exit
    """

    while True:
        print('Welcome to Yarn Genie! Your Magical Database for '
            'Crochet Patterns, Yarns and Hooks\n')
        print('1. View your patterns pieces.')
        print('2. View your yarn stash.')
        print('3. View your hook hoards.')
        print('4. Calculate what you can make!')
        print('5. Exit')

        user_input = input('\nPlease select an option by entering a number from 1 - 5\n')

        if user_input == '1':
            show_worksheet('patterns')
            sub_menu('pattern', get_user_data, remove_from_worksheet)
        elif user_input == '2':
            show_worksheet('yarns')
            sub_menu('yarn', get_user_data, remove_from_worksheet)
        elif user_input == '3':
            show_worksheet('hooks')
            sub_menu('hook', get_user_data, remove_from_worksheet)
        elif user_input == '4':
            print('call function calculate')
        elif user_input == '5':
            print('Goodbye and stitch you later!')
            break
        else:
            print('Invalid option, please eneter a number from 1 - 5\n')
            input('Press Enter to continue...\n')

main_menu()