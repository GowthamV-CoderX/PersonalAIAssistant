from app.tools.executor import execute_tool


def run_tool_request(request: dict):
    if not isinstance(request, dict):
        raise ValueError("Tool request must be a dictionary.")

    tool_name = request.get("tool")
    arguments = request.get("arguments")

    if not isinstance(tool_name, str):
        raise ValueError("Tool name must be a string.")

    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be a dictionary.")

    return execute_tool(tool_name, arguments)