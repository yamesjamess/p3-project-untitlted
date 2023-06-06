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


# Worksheet Manipulation Functions
def show_worksheet(worksheet):
    """
    Print out a table of all the values from specific worksheet

    Args:
        worksheet: string: the name of the worksheet

    Returns:
        List of lists. Sublist contains row values of worksheet
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
    # turn list into table in the termial
    print(tabulate(stash))


def add_to_worksheet(data, worksheet):
    """
    Update relevant worksheet, add new row with list data provided.

    Args:
        data: list: CSV to be added to worksheet
        worksheet: string: the name of the worksheet
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

    Args:
        worksheet: string: the name of the worksheet
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
            index += 1
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


# User input functions
def get_user_data(type, num):
    """
    Get pattern/yarn/hook information input from user

    Args:
        type: string: the name of category of data user want to input
        num: int: display the length of csv user need to input
    Returns:
        list: result of user csv input or blank if the user chose to
        exit program
    """
    while True:
        if type == 'pattern' or type == 'yarn':
            print(f'\nPlease enter your {type} information.')
            print(f'\nInformation should be {num} categories, '
                  'separate by commas.')

        if type == 'pattern':
            print(f'\n{type.capitalize()} Name, Yarn Weight, '
                  'Yarn Length (m), Hook Size')
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
            print(f'\n{type.capitalize()} Name, Material, '
                  f'{type.capitalize()} Weight, {type.capitalize()} '
                  'Length, Colour, Quantity')
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

    Args:
        values: list: list of csv from get_user_data

    Returns:
        boolean: result of validation

    Raises:
        ValueError, if value is not equal to 4
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
    Check if the yarns input contains exactly 6 values

    Args:
        values: list: list of csv from get_user_data

    Returns:
        boolean: result of validation

    Raises:
        ValueError, if value is not equal to 6
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f'6 values required, you provided {len(values)}')

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
    Check if the patterns input contains exactly 1 values

    Args:
        values: list: list of csv from get_user_data

    Returns:
        boolean: result of validation

    Raises:
        ValueError, if value is not equal to 1
    """
    try:
        if len(values) != 1:
            raise ValueError(
                f'1 values required, you provided {len(values)}')
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True


# Calculation functions
def calculate(user_input):
    """
    Takes user input selection of pattern, then compare it against yarn and
    hook stock to see if the user meet the requirement to make that pattern
    or not.

    Args:
        user_input: list: list of values from selected row on worksheet

    Riases:
        ValueError: if input is not an integer
    """
    yarns_data = SHEET.worksheet('yarns').get_all_values()
    yarns_data.pop(0)
    header_removed = yarns_data

    hooks_data = SHEET.worksheet('hooks')
    hooks_size = hooks_data.col_values(1)
    hooks_size.pop(0)

    print('Calculating...\n')

    # check if the user has the hook required for the project
    if user_input[3] in hooks_size:
        print(f'You have {user_input[3]}mm hook to make this project!\n')
    else:
        print(f'This pattern requires a {user_input[3]}mm hook, '
              'you do not have the hook. Go buy some hook!\n')

    # checks if there are more than 1 yarn that matches the same weight
    # the user has selected
    matched_lists = [lst for lst in yarns_data if lst[2] == user_input[1]]
    # if there are more than 1 matches
    if len(matched_lists) > 1:
        print(f'You have more than 1 of {user_input[1]} yarn, '
              'please select a yarn you want to use\n')
        for i, lst in enumerate(matched_lists):
            print(f"Yarn {i+1}: {lst}")

        # asking the user to select which yarn they want to use
        # from the list above
        while True:
            try:
                selected_yarn = int(input('\nEnter the yarn number you want '
                                          'to use (1, 2, etc.): \n').strip())
                selected_yarn -= 1

                # print out the user's selection
                if selected_yarn >= 0 and selected_yarn < len(matched_lists):
                    selected_yarn_data = matched_lists[selected_yarn]
                    print(f"\nYou've selected a {selected_yarn_data[1]} "
                          f"{selected_yarn_data[2]} yarn by "
                          f"{selected_yarn_data[0]}'s in "
                          f"{selected_yarn_data[4]} colourway\n")
                    total_yarn_length = (int(selected_yarn_data[3]) *
                                         int(selected_yarn_data[5]))
                    # when user have more yarn than pattern requires
                    if total_yarn_length > int(user_input[2]):
                        print('Congratulations! You have enough yarn to make '
                              'this project!\n')
                        input('Press Enter to go back to main menu...\n')
                        break
                    # when user does not have enough yarn legnth
                    elif total_yarn_length < int(user_input[2]):
                        remaining_yarn = int(user_input[2]) - total_yarn_length
                        additional_ball = ((remaining_yarn +
                                            int(selected_yarn_data[3]) - 1)
                                           // int(selected_yarn_data[3]))
                        print(f'You have {selected_yarn_data[5]} ball(s) of '
                              f'{selected_yarn_data[3]}m yarn. You would need '
                              f'{additional_ball} more ball(s) '
                              'more to make this project. '
                              'Go and buy some more!\n')
                        input('Press Enter to go back to main menu...\n')
                        break
                else:
                    print("Invalid option. Please try again.\n")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # if there are only 1 match
    elif len(matched_lists) <= 1 and len(matched_lists) != 0:
        # matched_lists is a nested list
        # this turns it into a flat list for ease of computation
        yarn_data = []
        for sublist in matched_lists:
            yarn_data.extend(sublist)

        total_yarn_length = int(yarn_data[3]) * int(yarn_data[5])
        # when user have more yarn than pattern requires
        if total_yarn_length > int(user_input[2]):
            print('Congratulations! You have enough yarn to make '
                  'this project!\n')
            print(f"The yarn you will be using is {yarn_data[0]}'s "
                  f"{yarn_data[2]} {yarn_data[1]} yarn in "
                  f"{yarn_data[4]} colourway.\n")
            input('Press Enter to go back to main menu...\n')
            return
        # when user does not have enough yarn legnth
        elif total_yarn_length < int(user_input[2]):
            remaining_yarn = int(user_input[2]) - total_yarn_length
            additional_ball = ((remaining_yarn + int(yarn_data[3]) - 1) //
                               int(yarn_data[3]))

            print(f'You have {yarn_data[5]} ball(s) of '
                  f'{yarn_data[3]}m yarn. You would need '
                  f'{additional_ball} more ball(s) '
                  'more to make this project. Go and buy some more yarns!\n')
            input('Press Enter to go back to main menu...\n')
            return
    else:
        print(f"To make this pattern, you'd need {user_input[1]}"
              " weight yarn.\n"
              "You don't have any of them in your stash.\n"
              "You should go and buy some yarns!\n")
        input('Press Enter to go back to main menu...\n')
        return


# Menu functions
def calc_menu():
    """
    Display pattern selection and and back to sub menu until the user
    select a valid option, then calls the requested function
    """

    show_worksheet('patterns')
    pattern = SHEET.worksheet('patterns')
    patterns_list = pattern.get_all_values()
    patterns_list.pop(0)

    selected_row = input('\nPlease enter a number to select a pattern or '
                         'enter "x" to return to the main menu\n').strip()

    while True:
        if selected_row.upper() == 'X':
            print('\nReturning to the main menu')
            input('\nPress Enter to continue...\n')
            break
        elif selected_row.isdigit() and (0 < int(selected_row) <=
                                         len(patterns_list)):
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
            selected_row = input('Enter a number or enter "x"'
                                 ' to cancel...\n').strip()


def sub_menu(str, worksheet, add_func, remove_func):
    """
    Display add, remove, and back sub menu until the user select a valid option
    then calls the requested funcion

    Args:
        str: string: title of the submenu (patterns/yarns/hooks)
        worksheet: string: name of the worksheet on the spreadsheet
        add_func: function: calls add_function
        remove_func: function: calls remove function
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

        user_input = input('\nPlease select an option by '
                           'entering a number from 1, 2, or 3\n').strip()

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
    """
    ASCII text art of the program
    """
    print("                                          .-.                     ")
    print("  .-.   .-                         .--.`-'               .-.      ")
    print("    /  (  .-.    ).--. .  .-.     /  (_;    .-..  .-.    `-' .-.  ")
    print("   (    )(  |   /       )/   )   /        ./.-'_)/   )  /  ./.-'_ ")
    print(" .  `..'  `-'-'/       '/   (   (     --;-(__.''/   (_.(__.(__.'  ")
    print("(__.-'                       `-  `.___.'             `-           "
          "\n")


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

        user_input = input('\nPlease select an option by entering a '
                           'number from 1 - 5\n').strip()

        if user_input == '1':
            sub_menu('pattern', 'patterns', get_user_data, remove_item)
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


if __name__ == "__main__":
    main_menu()
