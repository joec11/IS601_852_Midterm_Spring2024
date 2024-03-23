'''Testing the divide plugin'''
# pylint: disable=unused-variable"
import pytest
from app import App
from app.plugins import divide

def test_app_divide_plugin(monkeypatch):
    """Test that the REPL correctly handles the 'divide' plugin and returns the division of two operands."""
    inputs = iter(['divide', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    # Check that the exit was graceful with the correct exit code
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

    # Assert that 'divide' plugin works correctly
    assert divide.DivideCommand.execute('divide', 18, 6) == 3, "The 'divide' plugin did not work correctly."
