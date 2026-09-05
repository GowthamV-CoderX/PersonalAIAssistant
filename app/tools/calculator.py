def calculate(a: float, b: float, operation: str) -> float:
    """
    Perform a basic arithmetic operation.
    """

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")

        return a / b

    raise ValueError(f"Unsupported operation: {operation}")


def calculator_tool(a: float, b: float, operation: str) -> float:
    """
    Calculate a mathematical expression using two numbers.

    Args:
        a: First number.
        b: Second number.
        operation: One of add, subtract, multiply, or divide.

    Returns:
        The calculated result.
    """

    return calculate(a, b, operation)