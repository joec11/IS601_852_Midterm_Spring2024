from app.commands import Command
from calculator import subtract

class SubtractCommand(Command):
    def execute(self, *args):
        return subtract(args[0], args[1])
