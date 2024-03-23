'''My Calculator Test with pytest fixture'''
from decimal import Decimal
import pytest

# Import Calculation and Calculations classes from the calculator package.
from calculator.calculation import Calculation
from calculator.calculations import Calculations

# Import arithmetic operation functions (add, subtract, multiply, and divide) to be tested.
from calculator.operations import add, subtract, multiply, divide

# pytest.fixture is a decorator that marks a function as a fixture,
# a setup mechanism used by pytest to initialize a test environment.
# Here, it's used to define a fixture that prepares the test environment for calculations tests.
@pytest.fixture
def setup_calculations():
    """Clear history and add sample calculations for tests."""
    # Clear any existing calculation history to ensure a clean state for each test.
    Calculations.clear_history()
    # Add sample calculations to the history to set up a known state for testing.
    # These calculations represent typical use cases and allow tests to verify that
    # the history functionality is working as expected.
    Calculations.add_calculation(Calculation(Decimal('10'), Decimal('5'), add))
    Calculations.add_calculation(Calculation(Decimal('20'), Decimal('3'), subtract))
    Calculations.add_calculation(Calculation(Decimal('7'), Decimal('4'), multiply))
    Calculations.add_calculation(Calculation(Decimal('28'), Decimal('7'), divide))

def test_add_calculation(setup_calculations):
    """Test adding a calculation to the history."""
    # Create a new Calculation object to add to the history.
    calc = Calculation(Decimal('2'), Decimal('2'), add)
    # Add the calculation to the history.
    Calculations.add_calculation(calc)
    # Assert that the calculation was added to the history by checking
    # if the latest calculation in the history matches the one we added.
    assert Calculations.get_latest() == calc, "Failed to add the calculation to the history"

def test_get_history(setup_calculations):
    """Test retrieving the entire calculation history."""
    # Retrieve the calculation history.
    history = Calculations.get_history()
    # Assert that the history contains exactly 4 calculations,
    # which matches our setup in the setup_calculations fixture.
    assert len(history) == 4, "History does not contain the expected number of calculations"

def test_clear_history(setup_calculations):
    """Test clearing the entire calculation history."""
    # Clear the calculation history.
    Calculations.clear_history()
    # Assert that the history is empty by checking its length.
    assert len(Calculations.get_history()) == 0, "History was not cleared"

def test_get_latest(setup_calculations):
    """Test getting the latest calculation from the history."""
    # Retrieve the latest calculation from the history.
    latest = Calculations.get_latest()
    # Assert that the latest calculation matches the expected values,
    # specifically the operands and operation used in the last added calculation
    # in the setup_calculations fixture.
    assert latest.a == Decimal('28') and latest.b == Decimal('7'), "Did not get the correct latest calculation"

def test_find_by_operation(setup_calculations):
    """Test finding calculations in the history by operation type."""
    # Find all calculations with the 'add' operation.
    add_operations = Calculations.find_by_operation("add")
    # Assert that exactly one calculation with the 'add' operation was found.
    assert len(add_operations) == 1, "Did not find the correct number of calculations with add operation"
    # Find all calculations with the 'subtract' operation.
    subtract_operations = Calculations.find_by_operation("subtract")
    # Assert that exactly one calculation with the 'subtract' operation was found.
    assert len(subtract_operations) == 1, "Did not find the correct number of calculations with subtract operation"
    # Find all calculations with the 'multiply' operation.
    multiply_operations = Calculations.find_by_operation("multiply")
    # Assert that exactly one calculation with the 'multiply' operation was found.
    assert len(multiply_operations) == 1, "Did not find the correct number of calculations with multiply operation"
    # Find all calculations with the 'divide' operation.
    divide_operations = Calculations.find_by_operation("divide")
    # Assert that exactly one calculation with the 'divide' operation was found.
    assert len(divide_operations) == 1, "Did not find the correct number of calculations with divide operation"

def test_get_latest_with_empty_history():
    """Test getting the latest calculation when the history is empty."""
    # Ensure the history is empty by clearing it.
    Calculations.clear_history()
    # Assert that the latest calculation is None since the history is empty.
    assert Calculations.get_latest() is None, "Expected None for latest calculation with empty history"
