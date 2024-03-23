'''Testing the add plugin'''
# pylint: disable=unused-variable"
import pytest
from app import App
from app.plugins import add

def test_app_add_plugin(monkeypatch):
    """Test that the REPL correctly handles the 'add' plugin and returns the sum of two operands."""
    inputs = iter(['add', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    # Check that the exit was graceful with the correct exit code
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

    # Assert that 'add' plugin works correctly
    assert add.AddCommand.execute('add', 2, 2) == 4, "The 'add' plugin did not work correctly."
