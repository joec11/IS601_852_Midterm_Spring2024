import os
import pkgutil
import importlib
from app.commands import CommandHandler, Command
from dotenv import load_dotenv, dotenv_values
import logging
import logging.config
from decimal import Decimal, InvalidOperation

class App:
    def __init__(self): # Constructor
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def configure_logging(self):
        """Configure Logging to allow logging application activity"""
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")
    
    def load_environment_variables(self):
        """Load the environment variables from the env file"""
        if os.path.exists(".env"):
            logging.info("Environment variables loaded from .env file."); \
            return dotenv_values(".env")
        else:
            logging.warning("The .env file does not exist. Operating system environment variables loaded."); \
            return {key: value for key, value in os.environ.items()}

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        """Get environment variable"""
        return self.settings.get(env_var, None)

    def load_plugins(self):
        """Load Plugins"""
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found."); \
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module, plugin_name):
        """Register the plugin commands"""
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                # Command names are now explicitly set to the plugin's folder name
                self.command_handler.register_command(plugin_name, item())
                logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")

    def start(self):
        """Start method"""
        self.load_plugins()
        logging.info("Application started.")
        print("Type 'menu' to get a list of commands.\
              \nType 'csv' to manage history of calculations.\
              \nType 'exit' to exit.")

        commandList = [command for command in self.command_handler.commands.keys()]
        self.command_handler.execute_command(commandList, "menu") if 'menu' in commandList else None

        while True:
            cmd_input = input(">>> ").strip().split()
            try:
                assert 0 < len(cmd_input) <= 3

                a_decimal, b_decimal = (map(Decimal, cmd_input[:2]) if len(cmd_input) > 2 else (Decimal(0.0), Decimal(1.0)))
                command = cmd_input[-1]

                result = self.command_handler.execute_command(commandList, "menu") if command.lower() == 'menu' \
                else self.command_handler.execute_command(a_decimal, b_decimal, command)

                if (len(cmd_input) > 2 and result is not None):
                    logging.info(f"{a_decimal} {b_decimal} {command} = {result}"); \
                    print(result); \
                    self.command_handler.execute_command(a_decimal, b_decimal, command, result, "csv") if "csv" in commandList else None
            except AssertionError:
                logging.error("Usage: <number1> <number2> <operation/command> | <command>"); \
                print("Usage: <number1> <number2> <operation/command> | <command>")
            except KeyError:  # Assuming execute_command raises KeyError for unknown commands
                logging.error(f"Unknown command: {cmd_input}"); \
                print(f"Unknown command: {cmd_input}")
            except InvalidOperation:
                logging.error("Invalid Operation"); \
                print("Invalid Operation")
            except ValueError as e:
                logging.error(e); \
                print(e)
