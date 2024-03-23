import logging
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from app.commands import Command

class CsvCommand(Command):
    def execute(self, *args):
        try:
            load_dotenv(find_dotenv())
            data_dir = os.path.abspath(os.getenv('DATA_DIR', 'data')); \
            csv_file_path = os.path.join(data_dir, os.getenv('CALC_HISTORY_CSV', 'calculations_history.csv'))
            
            if not os.path.exists(data_dir): \
                os.makedirs(data_dir)

            if not os.path.exists(csv_file_path): \
                open(csv_file_path, "w").close()

            if not os.access(data_dir, os.W_OK) or not os.access(csv_file_path, os.W_OK): \
                raise OSError

            if len(args) == 5: \
                pd.DataFrame({'A': [args[0]], 'B': [args[1]], 'CMD': [args[2]], 'Result': [args[3]]}) \
                    .to_csv(csv_file_path, mode='a', header=False, index=False); \
                return

            df_calculations = pd.read_csv(csv_file_path, header=None, names=['1st Operand', '2nd Operand', 'Command', 'Result'])

            logging.info("Date file management started.")
            print("Type 'history' for a history of calculations.\
                \nType 'delete' followed by the row number(s) to delete specific row(s).\
                \nType 'clear' to clear the entire history of calculations.\
                \nType 'done' to exit calculation history management.\n")
            print("History is blank." if df_calculations.empty else df_calculations)

            done = False
            while not done:
                option_input = input(">>>>>> ").strip().split()
                try:
                    assert 0 < len(option_input) <= len(df_calculations.index) + 1

                    option = option_input[0].lower(); \
                    rows_to_delete = [int(x) for x in option_input[1:]] if (len(option_input) > 1 and option == 'delete') else []

                    match option:
                        case "clear":
                            if input("Are you sure you want to clear all records? (Y/N) ").lower() == 'y': \
                                df_calculations.drop(df_calculations.index, inplace=True); \
                                logging.info("All records have been deleted from the calculation history."); \
                                print("All records have been deleted from the calculation history."); \
                                df_calculations.to_csv(csv_file_path, header=False, index=False)
                        case "delete":
                            if df_calculations.index.isin(rows_to_delete).any(): \
                                df_calculations.drop(rows_to_delete, axis=0, inplace=True); \
                                logging.info("Records deleted from the calculation history: %s", rows_to_delete); \
                                print("Records deleted from the calculation history:", rows_to_delete); \
                                df_calculations.to_csv(csv_file_path, header=False, index=False)
                        case "done":
                            done = True; \
                            logging.info("Date file management ended."); \
                            print("Returned back to main menu.")
                        case "history":
                            print("History is blank." if df_calculations.empty else df_calculations)
                        case _:
                            pass
                except AssertionError:
                    logging.error("Usage: <option> | delete [<row-number(s)>]"); \
                    print("Usage: <option> | delete [<row-number(s)>]")
                except ValueError:
                    logging.error(f"Invalid literal(s) - delete can only be followed by integer(s)"); \
                    print(f"Invalid literal(s) - delete can only be followed by integer(s)")
        except OSError:
            logging.error(f"Either the data directory '{data_dir}' or the data file '{csv_file_path}' is not writable.")
