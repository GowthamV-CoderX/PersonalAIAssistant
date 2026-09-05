from app.tools.calculator import calculate


TOOLS = {
    "calculator": calculate,
}


def get_tool(name: str):
    return TOOLS.get(name)


def list_tools() -> list[str]:
    return list(TOOLS.keys())