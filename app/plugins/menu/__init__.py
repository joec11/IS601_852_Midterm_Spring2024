import logging
from app.commands import Command

class MenuCommand(Command):
    def execute(self, *args):
        logging.info(f"Menu command entered. List of commands: {args[0]}")
        print("\nList of commands:")
        [print(item, end='\n') for item in args[0]]
