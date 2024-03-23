'''Testing the greet plugin'''
# pylint: disable=unused-variable"
import pytest
from app import App

def test_app_greet_plugin(capfd, monkeypatch):
    """Test that the REPL correctly handles the 'greet' plugin and outputs 'Hello, World!'."""
    inputs = iter(['greet', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    # Check that the exit was graceful with the correct exit code
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

    # Capture the output from the 'greet' plugin
    out, err = capfd.readouterr()

    # Assert that "Hello! Thank you for using this application." was printed to stdout
    assert "Hello! Thank you for using this application." in out, "The 'greet' plugin did not produce the expected output."
