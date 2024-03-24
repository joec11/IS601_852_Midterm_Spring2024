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

    def clear_option(self):
        if input("Are you sure you want to clear all records? (Y/N) ").lower() == 'y': \
            self.df_calculations.drop(self.df_calculations.index, inplace=True); \
            logging.info("All records have been deleted from the calculation history."); \
            print("All records have been deleted from the calculation history."); \
            self.df_calculations.to_csv(self.csv_file_path, header=False, index=False)

    def delete_option(self, *args):
        if self.df_calculations.index.isin(*args).any(): \
            self.df_calculations.drop(*args, axis=0, inplace=True); \
            logging.info("Records deleted from the calculation history: %s", *args); \
            print("Records deleted from the calculation history:", *args); \
            self.df_calculations.to_csv(self.csv_file_path, header=False, index=False)

    def done_option(self):
        self.done = True; \
        logging.info("Date file management ended."); \
        print("Returned back to main menu.")

    def history_option(self):
        print("History is blank." if self.df_calculations.empty else self.df_calculations)

    def execute(self, *args):
        try:
            load_dotenv(find_dotenv())
            self.data_dir = os.path.abspath(os.getenv('DATA_DIR', 'data')); \
            self.csv_file_path = os.path.join(self.data_dir, os.getenv('CALC_HISTORY_CSV', 'calculations_history.csv'))
            
            if not os.path.exists(self.data_dir): \
                os.makedirs(self.data_dir)

            if not os.path.exists(self.csv_file_path): \
                open(self.csv_file_path, "w").close()

            if not os.access(self.data_dir, os.W_OK) or not os.access(self.csv_file_path, os.W_OK): \
                raise OSError

            if len(args) == 5: \
                pd.DataFrame({'A': [args[0]], 'B': [args[1]], 'CMD': [args[2]], 'Result': [args[3]]}) \
                    .to_csv(self.csv_file_path, mode='a', header=False, index=False); \
                return

            self.df_calculations = pd.read_csv(self.csv_file_path, header=None, names=['1st Operand', '2nd Operand', 'Command', 'Result'])

            logging.info("Date file management started.")
            print("Type 'history' for a history of calculations.\
                \nType 'delete' followed by the row number(s) to delete specific row(s).\
                \nType 'clear' to clear the entire history of calculations.\
                \nType 'done' to exit calculation history management.\n")
            self.history_option()

            while not self.done:
                option_input = input(">>>>>> ").strip().split()
                try:
                    assert 0 < len(option_input) <= len(self.df_calculations.index) + 1

                    option = option_input[0].lower(); \
                    rows_to_delete = [int(x) for x in option_input[1:]] if (len(option_input) > 1 and option == 'delete') else []

                    match option:
                        case "clear":
                            self.clear_option()
                        case "delete":
                            self.delete_option(rows_to_delete)
                        case "done":
                            self.done_option()
                        case "history":
                            self.history_option()
                        case _:
                            pass
                except AssertionError:
                    logging.error("Usage: <option> | delete [<row-number(s)>]"); \
                    print("Usage: <option> | delete [<row-number(s)>]")
                except ValueError:
                    logging.error(f"Invalid literal(s) - delete can only be followed by integer(s)"); \
                    print(f"Invalid literal(s) - delete can only be followed by integer(s)")
            self.done = False
        except OSError:
            logging.error(f"Either the data directory '{self.data_dir}' or the data file '{self.csv_file_path}' is not writable.")
