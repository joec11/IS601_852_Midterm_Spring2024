from app.commands import Command
from calculator import multiply

class MultiplyCommand(Command):
    def execute(self, *args):
        return multiply(args[0], args[1])
