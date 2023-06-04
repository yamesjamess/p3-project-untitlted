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


def clear():
    """
    clears the terminal
    """
    print('\033c')

# Worksheet Manipulation Section
def show_worksheet(worksheet):
    """
    Print out a table of all the values from specific worksheet
    """
    clear()
    print(f'You have the following {worksheet} in your stash!\n')
    stash = SHEET.worksheet(worksheet).get_all_values()
    num = 0

    for index, row in enumerate(stash):
        if index == 0:
            row.insert(0, '')
        else:
            row.insert(0, index)

    print(tabulate(stash))

def add_to_worksheet(data, worksheet):
    """
    Update relevant worksheet, add new row with list data provided.
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully!\n')
    input('Press Enter to add another item...\n')

    if worksheet == 'patterns':
        clear()
        show_worksheet(worksheet)
    elif worksheet == 'yarns':
        clear()
        show_worksheet(worksheet)
    elif worksheet == 'hooks':
        clear()
        show_worksheet(worksheet)


def remove_item(worksheet):
    """
    Remove a row the user has selected from the relevant worksheet.
    """
    print(f'\nWhich item do you want to from your {worksheet} list?\n')
    worksheet_to_remove = SHEET.worksheet(worksheet)
    user_input = input('Enter a number or enter "x" to cancel...\n')

    while True:
        if user_input.upper() == 'X':
            print('\nReturning to the sub-menu')
            input('\nPress Enter to continue...\n')
            break
        elif user_input.isdigit() and user_input != '0':
            index = int(user_input)
            index +=1
            worksheet_to_remove.delete_rows(index)
            print(f'\nItem {user_input} has been removed!')
            input('\nPress Enter to continue...\n')
            break
        elif user_input == '0':
            print('\nInvalid option, please try again...')
            user_input = input('Enter a number or enter "x" to cancel...\n')
        else:
            print('\nInvalid option, please try again...')
            user_input = input('Enter a number or enter "x" to cancel...\n')


# User input section
def get_user_data(type, num):
    """
    Get pattern/yarn/hook information input from user
    """
    while True:
        if type == 'pattern' or type == 'yarn':
            print(f'\nPlease enter your {type} information.')
            print(f'\nInformation should be {num} categories, separate by commas.')

        if type == 'pattern':
            print(f'\n{type.capitalize()} Name, Yarn Weight, Yarn Length (m), Hook Size')
            print('Example: Kids Gloves, Double Knit, 400, 3.00\n')

            pattern_data = input(f'Enter your {type} information here '
                                'or enter "x" to return to sub-menu:\n')
            if pattern_data.upper() == 'X':
                print('Returning to sub-menu\n')
                show_worksheet('patterns')
                return []

            pattern_info = [value.strip() for value in pattern_data.split(',')]
            if validate_pattern(pattern_info):
                print('\nInformation is valid!\n')
                add_to_worksheet(pattern_info, 'patterns')

        elif type == 'yarn':
            print(f'\n{type.capitalize()} Name, Material, {type.capitalize()} Weight, {type.capitalize()} Length, Colour, Quantity')
            print('Example: Rico, Cotton, Double Knit, 200, Teal, 1\n')

            yarn_data = input(f'Enter your {type} information here '
                                'or enter "x" to return to sub-menu:\n')
            if yarn_data.upper() == 'X':
                print('Returning to sub-menu\n')
                show_worksheet('yarns')
                return []

            yarn_info = [value.strip() for value in yarn_data.split(',')]
            if validate_yarn(yarn_info):
                print('\nInformation is valid!\n')
                add_to_worksheet(yarn_info, 'yarns')

        elif type == 'hook':
            print(f'\nPlease enter your {type} information.')
            print(f'\nInformation should be {num} category.')
            print(f"\nNote: Only add hooks that you've owned!")
            print(f'\n{type.capitalize()} Size')
            print('Example: 6.00\n')
            
            hook_data = input(f'Enter your {type} information here '
                                'or enter "x" to return to sub-menu:\n')

            if hook_data.upper() == 'X':
                print('Returning to sub-menu\n')
                show_worksheet('hooks')
                return []

            hook_info = [value.strip() for value in hook_data.split(',')]
            if validate_hook(hook_info):
                print('\nInformation is valid!\n')
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
        if len(values) != 6:
            raise ValueError(
                f'6 values required, you provided {len(values)}'    
            )
        
            # convert data at 3rd and 5th indices into intergers
            indices = [3, 5]
            for index in indices:
                values[index] = int(values[index])
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True


def validate_hook(values):
    """
    Check if user has input the correct values for hooks3
    """
    try:
        if len(values) != 1:
            raise ValueError(
                f'1 values required, you provided {len(values)}'    
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True


# Calculation functions
def calculate(user_input):
    # clear()
    """
    Takes user input selection of pattern, then compare it against yarn and 
    hook stock to see if the user meet the requirement to make that pattern
    or not.
    """
    yarns_data = SHEET.worksheet('yarns')
    yarn_weight = yarns_data.col_values(3)
    yarn_length = yarns_data.col_values(4)
    yarn_quantity = yarns_data.col_values(6)
    yarn_weight.pop(0)
    yarn_length.pop(0)
    yarn_quantity.pop(0)
    
    
    hooks_data = SHEET.worksheet('hooks')
    hooks_size = hooks_data.col_values(1)
    hooks_size.pop(0)

    if user_input[3] in hooks_size:
        print(f'You have {user_input[3]}mm hook to make this project!\n')
    else:
        print(f'This pattern require a {user_input[3]}mm hook, ' 
            'you dont have the hook. Go buy some!')

    print('Calculating...\n')

    print(user_input)




    
   

    #this part does the calculation if you have the same weight yarn

    # if data[1].lower() in [item.lower() for item in yarn_weight]:
    #     # if you have enough length
    #     if:
    #     print(f'{data[1]} exist')
    # else:
    #     print(f'{data[1]} does not exist')

    
    #if you have the same size hook


def calc_menu():
    """
    Display pattern selection and and back to sub menu until the user
    select a valid option, then calls the requested function
    """

    show_worksheet('patterns')
    pattern = SHEET.worksheet('patterns')

    selected_row = input('\nPlease enter a number to select a pattern or enter '
                        '"x" to return to the main menu\n')

    while True:
        if selected_row.upper() == 'X':
            print('\nReturning to the main menu')
            input('\nPress Enter to continue...\n')
            break
        elif selected_row.isdigit() and selected_row != '0':
            row = int(selected_row)
            row += 1
            data = pattern.row_values(row)
            print(f'\nYou have selected a {data[0]} pattern!\n')
            print(f'You will need a {data[1]} weighted yarn with the total ')
            print(f'legnth of {data[2]}m, and a size {data[3]}mm hook.\n')
            input('Press Enter to continue...\n')
            calculate(data)
            break
        else:
            print('\nInvalid option, please try again...')
            selected_row = input('Enter a number or enter "x" to cancel...\n')

# calculate()
# calc_menu()

def sub_menu(str, worksheet, add_func, remove_func):
    """
    Display add, remove, and back sub menu until the user select a valid option
    then calls the requested funcion
    
        Arguments:
            str: title of the submenu (patterns/yarns/hooks)
            worksheet: name of the worksheet on the spreadsheet
            add_func: calls add_function
            back_func: calls back function
    """
    while True:
        clear()
        if worksheet == 'patterns':
            show_worksheet(worksheet)
        elif worksheet == 'yarns':
            show_worksheet(worksheet)
        elif worksheet == 'hooks':
            show_worksheet(worksheet)

        print(f'\n1. Add a {str}')
        print(f'2. Remove a {str}')
        print(f'3. Go back to main menu')

        user_input = input('\nPlease select an option by entering a number from 1, 2, or 3\n')

        if user_input == '1':
            if str == 'pattern':
                get_user_data('pattern', 4)
            elif str == 'yarn':
                get_user_data('yarn', 6)
            elif str == 'hook':
                get_user_data('hook', 1)
        elif user_input == '2':
            if str == 'pattern':
                remove_item('patterns')
            elif str == 'yarn':
                remove_item('yarns')
            elif str == 'hook':
                remove_item('hooks')
        elif user_input == '3':
            break
        else:
            print('Invalid option, please eneter a number from 1, 2, or 3\n')
            input('Press Enter to continue...\n')


def art():
    print("                                         .-.                     ")
    print("  .-.   .-                        .--.`-'               .-.      ")
    print("    /  (  .-.    ).--..  .-.     /  (_;    .-..  .-.    `-' .-.  ")
    print("   (    )(  |   /      )/   )   /        ./.-'_)/   )  /  ./.-'_ ")
    print(" .  `..'  `-'-'/      '/   (   (     --;-(__.''/   (_.(__.(__.'  ")
    print("(__.-'                      `-  `.___.'             `-           \n")


def main_menu():
    """
    Display the main menu to the user until they select an option or exit
    """

    while True:
        clear()
        art()
        print('Welcome to Yarn Genie! A Magical Database for '
            'Crochet Patterns, Yarns and Hooks!\n')
        print('1. View your patterns pieces.')
        print('2. View your yarn stash.')
        print('3. View your hook hoards.')
        print('4. Calculate what you can make!')
        print('5. Exit')

        user_input = input('\nPlease select an option by entering a number from 1 - 5\n')

        if user_input == '1':
            sub_menu('pattern','patterns', get_user_data, remove_item)
        elif user_input == '2':
            sub_menu('yarn', 'yarns', get_user_data, remove_item)
        elif user_input == '3':
            sub_menu('hook', 'hooks', get_user_data, remove_item)
        elif user_input == '4':
            calc_menu()
        elif user_input == '5':
            print('Goodbye and stitch you later!')
            break
        else:
            print('Invalid option, please eneter a number from 1 - 5\n')
            input('Press Enter to continue...\n')


main_menu()
