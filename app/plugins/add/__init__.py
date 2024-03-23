from app.commands import Command
from calculator import add

class AddCommand(Command):
    def execute(self, *args):
        return add(args[0], args[1])
