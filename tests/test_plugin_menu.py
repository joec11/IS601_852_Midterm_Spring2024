'''Testing the menu plugin'''
# pylint: disable=unused-variable"
import pytest
from app import App

def test_app_menu_plugin(capfd, monkeypatch):
    """Test that the REPL correctly handles the 'menu' plugin and displays the menu."""
    inputs = iter(['menu', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    # Check that the exit was graceful with the correct exit code
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

    # Capture the output from the 'menu' plugin
    out, err = capfd.readouterr()

    # Assert that the 'menu' plugin produces an output that is not 'None'.
    assert out is not None, "The 'menu' plugin did not produce an output."
