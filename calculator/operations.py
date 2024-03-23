from decimal import Decimal
from typing import Union
# Define the functions with type hints
def add(a: Decimal, b: Decimal) -> Decimal:
    return a + b

def subtract(a: Decimal, b: Decimal) -> Decimal:
    return a - b

def multiply(a: Decimal, b: Decimal) -> Decimal:
    return a * b

def divide(a: Decimal, b: Decimal) -> Union[Decimal, str]:
    if b == 0:
        return "ERR: Divide by 0"
    return a / b
