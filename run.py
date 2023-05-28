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
    print(f'\nThe information provided is {yarn_data}') #need to colourise yarn data

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
