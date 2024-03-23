'''Testing the exit plugin'''
# pylint: disable=unused-variable"
import pytest
from app import App

def test_app_exit_plugin(monkeypatch):
    """Test that the REPL correctly handles the 'exit' plugin and exits."""
    inputs = iter(['exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    # Check that the exit was graceful with the correct exit code
    assert str(e.value) == "Exiting...", "The app did not exit as expected"
