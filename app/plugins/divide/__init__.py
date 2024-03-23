from app.commands import Command
from calculator import divide

class DivideCommand(Command):
    def execute(self, *args):
        return divide(args[0], args[1])
