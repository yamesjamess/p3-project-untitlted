import gspread
from google.oauth2.service_account import Credentials

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

def get_yarn_data():
    """
    Get yarn information input from user
    """
    print('Please enter your yarn information.')
    print('\nInformation should be 6 categories, separate by commas.')
    print('Yarn Name, Material, Yarn Weight, Yarn Length, Colour, Quantity')
    print('Example: Rico, Cotton, Double Knit, 200, Teal, 1\n')

    yarn_data = input('Enter your yarn information here: \n')
    
    yarn_info = yarn_data.split(',')
    validate_data(yarn_info)

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


get_yarn_data()

def main():
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
            print('call function show_yarns')
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
