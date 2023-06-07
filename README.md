<h1 align="center">Yarn Genie</h1>

[View the live project here](https://yarn-genie.herokuapp.com/)

![Yarn Genie](documentation/support_images/yarn_genie_terminal.png)

Yarn Genie is a terminal based application to manage crochet related data such as patterns, yarns, and hooks.

The user can utilise the application to view the data, add data to the database, remove the data, and calculate pattern requirements.

All the data are stored in Google Sheets and is accessed through API.

## Table of Contents
* [User Experience](#user-experience)
* [Features](#features)
* [Design](#design)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)

## User Experience

### As a user, I want to be able to :

1. Identify what is the purpose of the program.
2. Easily navigate through the different functionalities of the program.
3. Use the program to see the patterns/yarns/hooks I have in the database.
4. Use the program to add/remove patterns/yarns/hooks to and from the database
5. Check to see what I can make based on my pattern selection, this information should include :
    * if I have the yarn with the same weight as required in the pattern.
    * if I have enough yarn to make this pattern.
    * if I don't have enough, how much more do I need?
    * if I have the hook required to make the pattern.
    * if I don't have the hook, which size hook do I need?
6. Successfully use the program without encountering any errors.

## Features

### Existing Features

* __Main Menu & ASCII Art__

    * The ASCII art and the main menu are displayed when the user starts the program.
    * The particular font used to create the art conveys the feeling that the letters are made from stitches and have a slightly whimsical and magical quality to them.
    * The main menu is simple and easy for the user to understand. The main menu contains 5 options for the user to choose from : 
        1. Patterns-related actions
        2. Yarns-related actions
        3. Hooks-related actions
        4. Calculate action
        5. Exit program

        <br>
    * The user is prompted to select an option by entering a number respective to the options. If the user enters an incorrect value, an error message will be displayed and prompt the user to re-enter their option.
    * The main menu will keep running until the user selected a valid option or decided to terminate the program.
    
    <br>

* __Show Worksheet__

    * The function shows the data in a tabulated form for the user to see what Patterns/Yarns/Hooks they have in the database.
    * Underneath the table, the sub-menu is displayed for the user to select which actions they want to execute.

    <br>

* __Sub-Menu__ 

    * The sub-menu is executed once the user selected a valid option from the main menu.
    * The sub-menu is the same for Patterns/Yarns/Hooks to provide continuity for a better user experience.
    * The sub-menu contains 3 options for the user to select from :
        1. Add Pattern/Yarn/Hook
        2. Remove Pattern/Yarn/Hook
        3. Return to main menu
    * The Add and Remove functions can only be selected via the sub-menu.
    * Option 3 takes the user back to the main menu.
    
    <br>

* __Add Menu__

    * When the user selects the 1st option from the sub-menu, the get_user_data function is called.
    * The user will then be prompted to add data in a Comma Separate Value (CSV) format. An example will be shown above the input field to aid the user with the data entry process
    * The user's input will then be validated;
        * If the user's input is valid, the data will be added to the spreadsheet.
        * If the user's input is invalid, the user will be prompted to re-enter the data.
    * After the user has entered valid data, the user will then be prompted to continue the program, and the updated table with the most recently entered data will be displayed.

    <br>

* __Remove Menu__

    * When the user selects the 2nd option from the sub-menu, the remove_item function is called.
    * The user will then be prompted to select a row of data they want to be removed from the database.
    * The user's input will then be validated;
        * If the user's input is valid, the data will be deleted from the spreadsheet.
        * If the user's input is invalid, the user will be prompted to re-enter the data.
        
    <br>

* __Calculate Menu__

    * The function is executed when the user selected the 4th option from the main menu.
    * The user will be prompted to select a pattern from the database.
    * After the selection the program will then calculate these scenarios :
        * Does the user have the correct weight yarn to complete this pattern?
            * TRUE: print out the yarn that will be used. If there is more than 1 match, the user will be prompted to input an option to select from a list. Then move on to the next validation.
                * Does the user have enough of the yarn?
                    * TRUE: print out a message that the user can make this pattern.
                    * FALSE: print out a message that the urges user to go buy more yarn.
            * FALSE: print out a message that the user does not have the correct yarn weight and a message that urges the user to go buy more yarn.
        * Does the user have the correct size hook to complete this pattern?
            * TRUE: print out a message that the user have the correct size hook for the pattern.
            * FALSE: print out a message that the user does not have the correct size hook for the pattern, and urges them to go buy some.

    <br>

### Feature that could be implemented in the future

* __Graphic User Interface (GUI)__

    * Since the program is run exclusively in the terminal, it is not very user friendly for a human user that has no knowledge of operating the terminal. A web-based or executable program will be more intuitive for the user.

* __Data Duplication Validation__

    * The current version of the program allows the user to enter duplicate data, such as the same yarn multiple times. When Data Duplication Validation is implemented, it can detect duplications in the data and merge them when applicable.

<br>

## Technologies Used


### Languages Used
* [Python 3.11.1](https://www.python.org/downloads/release/python-3111/)

### Frameworks, Libraries & Programs Used
* [Google Spreadsheets]

* [Google Drive API]

* [Google Sheets API]

* [gspread]

* [Google Auth]

* [Lucid Chart]

* [patorjk.com Text to ASCII art](https://patorjk.com/software/taag/)

* [Git]: was used for version controlling purposes through git commands via the terminal on GitPod and is pushed to GitHub for cloud-based storage.

* [GitHub]: is used to host the repository of the project and is also used for the deployment of the website.

## Credits

### Contents
* The Google Spreadsheet "Yarn Genie" that this application ulitised is created by the developer
    * Pattern and Yarn data are gathered from [Ravelry](https://www.ravelry.com/)

* The inspiration for this application comes from [Elaine Broche's MS3 Event Scheduler](https://github.com/elainebroche-dev/ms3-event-scheduler) and [Alex Kavanagh's Grocery List Generator](https://github.com/alexkavanagh-dev/grocery_list_generator)

* Printing list into tabular data from [Stackoverflow](https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data)

* Different types of methods to access Google Sheet's data by [AO8](https://gist.github.com/AO8/d37a603f0121e8573dd0154595ab0460)

* How to use if name = main by [Geeks for Geeks](https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/)

* All other content was written by the developer

### Achknowledgements
* Thank you to my wonderful mentor, Brian Macharia, for helping me during all phases of the project.

* Special thanks to Code Institute Tutor, Sean, for helping me with coverting psedocode into actual code and also helping me from getting overwhelmed.