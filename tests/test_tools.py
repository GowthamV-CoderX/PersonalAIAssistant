import pytest

from app.tools.calculator import calculate
from app.tools.executor import execute_tool
from app.tools.protocol import run_tool_request
from app.tools.registry import get_tool, list_tools
from app.tools.router import route_tool


def test_calculator():
    assert calculate(847, 293, "multiply") == 248171


def test_division():
    assert calculate(100, 25, "divide") == 4


def test_division_by_zero():
    with pytest.raises(ValueError):
        calculate(10, 0, "divide")


def test_tool_registry():
    assert "calculator" in list_tools()
    assert get_tool("calculator") is not None


def test_tool_executor():
    result = execute_tool(
        "calculator",
        {
            "a": 847,
            "b": 293,
            "operation": "multiply",
        },
    )

    assert result == 248171


def test_unknown_tool():
    with pytest.raises(ValueError):
        execute_tool("unknown_tool", {})


def test_tool_protocol():
    result = run_tool_request(
        {
            "tool": "calculator",
            "arguments": {
                "a": 847,
                "b": 293,
                "operation": "multiply",
            },
        }
    )

    assert result == 248171


def test_router_calculation():
    assert route_tool("What is 847 * 293?") == 248171


def test_router_non_calculation():
    assert route_tool("What is machine learning?") is None