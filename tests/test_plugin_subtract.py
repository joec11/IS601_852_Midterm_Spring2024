'''Testing the subtract plugin'''
# pylint: disable=unused-variable"
import pytest
from app import App
from app.plugins import subtract

def test_app_subtract_plugin(monkeypatch):
    """Test that the REPL correctly handles the 'subtract' plugin and returns the difference of two operands."""
    inputs = iter(['subtract', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    # Check that the exit was graceful with the correct exit code
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

    # Assert that 'subtract' plugin works correctly
    assert subtract.SubtractCommand.execute('subtract', 2, 2) == 0, "The 'subtract' plugin did not work correctly."
