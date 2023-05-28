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

def get_yarn_info():
    """
    Get yarn information input from user
    """
    while True:
        print('Please enter your yarn information.')
        print('\nInformation should be 6 categories, separate by commas.')
        print('Yarn Name, Material, Yarn Weight, Yarn Length, Colour, Quantity')
        print('\nExample: Rico, Cotton, Double Knit, 200, Teal, 1\n')

        yarn_data = input('Enter your yarn information here: \n')
    
        yarn_info = yarn_data.split(',')
        
        if validate_data(yarn_info):
            print("\nInformation is valid!")
            break

    update_yarns_worksheet(yarn_info)


def validate_data(values):
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


def update_yarns_worksheet(data):
    """
    Update yarns worksheet, add new column with list data provided
    """
    print('Updating yarns worksheet...\n')
    yarns_worksheet = SHEET.worksheet('yarns')
    yarns_worksheet.append_row( data)
    print('Yarns worksheet updated successfully!\n')


def show_yarn():
    """
    Print out a table of all the values from specific worksheet
    """
        print('You have the following yarns in your stash!\n')
        stash = SHEET.worksheet('yarns').get_all_values()
        print(tabulate(stash))


def remove_yarn():
    print('remove yarn')


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
        show_yarn()
        print(f'\n1. Add {str}')
        print(f'2. Remove {str}')
        print(f'3. Go back to main menu')

        user_input = input('\nPlease select an option by entering a number from 1, 2, or 3\n')

        if user_input == '1':
            get_yarn_info()
        elif user_input == '2':
            remove_yarn()
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
            print('call function show_patterns')
        elif user_input == '2':
            sub_menu('a yarn', get_yarn_info, remove_yarn)
        elif user_input == '3':
            print('call function show_hooks')
        elif user_input == '4':
            print('call function calculate')
        elif user_input == '5':
            print('Goodbye and stitch you later!')
            break
        else:
            print('Invalid option, please eneter a number from 1 - 5\n')
            input('Press Enter to continue...\n')


def main():
    """
    Run all program functions
    """
    main_menu()



main()
