from ollama import chat

from app.tools.router import route_tool


MODEL = "qwen3:8b"

SYSTEM_PROMPT = """
You are Leny, a local personal AI assistant.

Your name is Leny.
Be concise and useful.
"""


def ask_leny(message: str) -> str:
    tool_result = route_tool(message)

    if tool_result is not None:
        return str(tool_result)

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        think=False,
        stream=False,
    )

    return response.message.content

