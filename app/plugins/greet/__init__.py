import logging
from app.commands import Command

class GreetCommand(Command):
    def execute(self, *args):
        logging.info("Greet command entered.")
        print(f"Hello! Thank you for using this application.")
