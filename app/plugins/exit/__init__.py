import logging
import sys
from app.commands import Command

class ExitCommand(Command):
    def execute(self, *args):
        logging.info("Exit command entered.")
        logging.info("Application shutdown.")
        sys.exit("Exiting...")
