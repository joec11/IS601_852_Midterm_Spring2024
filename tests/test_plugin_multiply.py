'''Testing the multiply plugin'''
# pylint: disable=unused-variable"
import pytest
from app import App
from app.plugins import multiply

def test_app_multiply_plugin(monkeypatch):
    """Test that the REPL correctly handles the 'multiply' plugin and returns the product of two operands."""
    inputs = iter(['multiply', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    # Check that the exit was graceful with the correct exit code
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

    # Assert that 'multiply' plugin works correctly
    assert multiply.MultiplyCommand.execute('multiply', 3, 4) == 12, "The 'multiply' plugin did not work correctly."
