from app.tools.registry import get_tool


def execute_tool(tool_name: str, arguments: dict):
    tool = get_tool(tool_name)

    if tool is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    try:
        return tool(**arguments)
    except TypeError as error:
        raise ValueError(
            f"Invalid arguments for tool '{tool_name}': {error}"
        ) from error