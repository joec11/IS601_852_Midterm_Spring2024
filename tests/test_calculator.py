'''My Calculator Test with the Calculator class'''
from calculator import Calculator

def test_addition():
    '''Test that the addition function works.'''
    assert Calculator.add(2, 2) == 4

def test_subtraction():
    '''Test that the subtraction function works.'''
    assert Calculator.subtract(2, 2) == 0

def test_multiplication():
    '''Test that the multiplication function works.'''
    assert Calculator.multiply(3, 4) == 12

def test_division():
    '''Test that the division function works.'''
    assert Calculator.divide(18, 6) == 3
