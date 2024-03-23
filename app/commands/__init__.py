from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self): \
        pass

class CommandHandler:
    def __init__(self): # Constructor
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        """Register Command"""
        self.commands[command_name] = command

    def execute_command(self, *args):
        """Execute Command"""
        return self.commands[args[-1]].execute(*args)
