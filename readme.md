# Midterm

## Implementation
Calculator:
    * Calculator Class:
        - Static methods: _perform_operation, add, subtract, multiply, divide

    * Calculation Class:
        - Class Constructor: __init__
        - Static method: create
        - Public method: perform
        - Special method: __repr__

    * Calculations Class:
        - history List of Calculation class objects
        - Class methods: add_calculation, get_history, clear_history, get_latest, find_by_operation

    * Operations:
        - Functions: add, subtract, multiply, divide

App:
    - Class Constructor: __init__
    - Public methods: configure_logging, load_environment_variables, get_environment_variable, load_plugins, register_plugin_commands, start

    Commands:
        * Command Class (Inherits from ABC):
            - Abstract method: execute
        
        * CommandHandler Class:
            - Class Constructor: __init__
            - Public methods: register_command, execute_command

    Plugins:
        * AddCommand Class (Inherits from Command):
            - Public method: execute

        * CsvCommand Class (Inherits from Command):
            - Class Constructor: __init__
            - Private methods: __clear_option, __delete_option, __done_option, __history_option, __perform, __set_data_path, __add_to_history
            - Public method: execute

        * DivideCommand Class (Inherits from Command):
            - Public method: execute

        * ExitCommand Class (Inherits from Command):
            - Public method: execute

        * GreetCommand Class (Inherits from Command):
            - Public method: execute

        * MenuCommand Class (Inherits from Command):
            - Public method: execute

        * MultiplyCommand Class (Inherits from Command):
            - Public method: execute

        * SubtractCommand Class (Inherits from Command):
            - Public method: execute

Data Directory (data):
    - Contains a calculations history csv file that stores calculations such as add, subtract, multiply, divide, and divide by zero.

GitHub Workflows:
    - Contains a python-app yml file that defines a workflow to install Python dependencies, run tests and lint with a single version of Python.

## Design Patterns
Look Before You Leap (LBYL):
    * App Class:
        - Checks if the logging configuration path exists, otherwise the default logging configuration will be used if the logging configuration path does not exist.
        - Checks if the environment variable file exists, otherwise the operating system environment variables will be loaded.

Easier to Ask for Forgiveness than Permission (EAFP):
    * App Class:
        - Uses a try/except to load and register a plugin, otherwise an import error will be logged stating that there was an error when trying to import the plugin.

        - Uses a try/except to:
            - Check if the user's input is greater than zero (0) and less than or equal to three (3), otherwise an assertion error will be logged and raised stating the expected user input.
            - Log and print a key error if the user enters an unknown command.
            - Log and print a invalid operation error if an invalid operation occurs.
            - Log and print a value error.

    * CsvCommand Class:
        - Uses a try/except to call the corresponding method based on the user input option, clear, delete, done, and history; otherwise an invalid user option exception will be displayed to the console.

        - Uses a try/except to:
            - Check if the user's input is greater than zero (0) and less than or equal to the total number if records in the calculation history csv file, otherwise an assertion error will be logged and raised stating the expected user input.
            - Log and print a value error for the delete option if the user attempts to enter a non-integer followed by delete.
            - Log an assertion error if either the data directory or the data file is not writable.

## Environment Variables
    * Environment variables are contained within the .env file and are loaded into the application when requested.
        - There are two environment variables that define the data directory and the data file name.
        - If the .env file does not exist or the requested environment variables are not found in the .env, then the default values will be used.

## Logging
    * Logging is configured to only log application activity to a log file and consists of the severity types, info, warning, and error.
