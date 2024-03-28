import logging
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from app.commands import Command

class CsvCommand(Command):
    def __init__(self):
        self.done = False

        self.df_calculations = None
        self.data_dir = None
        self.csv_file_path = None

        self.options = {
            'clear': self.__clear_option,
            'delete': self.__delete_option,
            'done': self.__done_option,
            'history': self.__history_option
        }

    def __clear_option(self, *args):
        if input("Are you sure you want to clear all records? (Y/N) ").lower() == 'y': \
            self.df_calculations.drop(self.df_calculations.index, inplace=True); \
            logging.info("All records have been deleted from the calculation history."); \
            print("All records have been deleted from the calculation history."); \
            self.df_calculations.to_csv(self.csv_file_path, header=False, index=False)

    def __delete_option(self, *args):
        if self.df_calculations.index.isin(*args).any(): \
            self.df_calculations.drop(*args, axis=0, inplace=True); \
            logging.info("Records deleted from the calculation history: %s", *args); \
            print("Records deleted from the calculation history:", *args); \
            self.df_calculations.to_csv(self.csv_file_path, header=False, index=False)

    def __done_option(self, *args):
        self.done = True; \
        logging.info("Date file management ended."); \
        print("Returned back to main menu.")

    def __history_option(self, *args):
        print("History is blank." if self.df_calculations.empty else self.df_calculations)

    def __perform(self, option: str, *args):
        try:
            self.options[option](*args)  # Call the corresponding method
        except Exception:
            print(f"Invalid: {option}")

    def __set_data_path(self):
        load_dotenv(find_dotenv())
        self.data_dir = os.path.abspath(os.getenv('DATA_DIR', 'data')); \
        self.csv_file_path = os.path.join(self.data_dir, os.getenv('CALC_HISTORY_CSV', 'calculations_history.csv'))

        os.makedirs(self.data_dir, exist_ok=True); \
        open(self.csv_file_path, "w").close() if not os.path.exists(self.csv_file_path) else None

    def __add_to_history(self, *args):
        pd.DataFrame({'A': [args[0]], 'B': [args[1]], 'CMD': [args[2]], 'Result': [args[3]]}) \
            .to_csv(self.csv_file_path, mode='a', header=False, index=False)

    def execute(self, *args):
        try:
            self.__set_data_path()
            assert os.access(self.data_dir, os.W_OK) and os.access(self.csv_file_path, os.W_OK) == True

            if len(args) == 5: \
                self.__add_to_history(*args); \
                return

            self.df_calculations = pd.read_csv(self.csv_file_path, header=None, names=['1st Operand', '2nd Operand', 'Command', 'Result']); \
            self.df_calculations.index = self.df_calculations.index + 1

            logging.info("Date file management started.")
            print("Type 'history' for a history of calculations.\
                \nType 'delete' followed by the row number(s) to delete specific row(s).\
                \nType 'clear' to clear the entire history of calculations.\
                \nType 'done' to exit calculation history management.\n")
            self.__perform("history")

            while not self.done:
                option_input = input(">>>>>> ").strip().split()
                try:
                    assert 0 < len(option_input) <= len(self.df_calculations.index) + 1

                    option = option_input[0].lower(); \
                    rows_to_delete = [int(x) for x in option_input[1:]] if (len(option_input) > 1 and option == 'delete') else []

                    self.__perform(option, rows_to_delete)
                except AssertionError:
                    logging.error("Usage: <option> | delete [<row-number(s)>]"); \
                    print("Usage: <option> | delete [<row-number(s)>]")
                except ValueError:
                    logging.error(f"Invalid literal(s) - delete can only be followed by integer(s)"); \
                    print(f"Invalid literal(s) - delete can only be followed by integer(s)")
            self.done = False
        except AssertionError:
            logging.error(f"Either the data directory '{self.data_dir}' or the data file '{self.csv_file_path}' is not writable.")
