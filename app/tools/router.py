import re

from app.tools.executor import execute_tool
def detect_calculation(message: str) -> bool:
    """
    Detect whether a message appears to contain a basic arithmetic request.
    """

    arithmetic_symbols = r"[+\-*/×÷]"

    has_numbers = bool(re.search(r"\d", message))
    has_operator = bool(re.search(arithmetic_symbols, message))

    return has_numbers and has_operator



def parse_calculation(message: str) -> dict:
    """
    Parse a basic two-number arithmetic expression.
    """

    match = re.search(
        r"(-?\d+(?:\.\d+)?)\s*([+\-*/×÷])\s*(-?\d+(?:\.\d+)?)",
        message,
    )

    if not match:
        raise ValueError("Could not parse calculation.")

    a_text = match.group(1)
    operator = match.group(2)
    b_text = match.group(3)

    a = float(a_text) if "." in a_text else int(a_text) 
    b = float(b_text) if "." in b_text else int(b_text)
    operation_map = {
        "+": "add",
        "-": "subtract",
        "*": "multiply",
        "/": "divide",
        "×": "multiply",
        "÷": "divide",
    }

    return {
        "a": a,
        "b": b,
        "operation": operation_map[operator],
    }
    
    
    
    from app.tools.executor import execute_tool


def route_tool(message: str):
    """
    Detect, parse, and execute a calculator request.
    """

    if not detect_calculation(message):
        return None

    arguments = parse_calculation(message)

    return execute_tool(
        "calculator",
        arguments,
    )