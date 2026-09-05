from ollama import chat

from app.memory.conversation import ConversationMemory
from app.tools.router import route_tool


MODEL = "qwen3:8b"

SYSTEM_PROMPT = """
You are Leny, a local personal AI assistant.

Your name is Leny.
Be concise and useful.
"""


memory = ConversationMemory()


def ask_leny(message: str) -> str:
    tool_result = route_tool(message)

    if tool_result is not None:
        response_text = str(tool_result)

        memory.add_message("user", message)
        memory.add_message("assistant", response_text)

        return response_text

    memory.add_message("user", message)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    messages.extend(memory.get_messages())

    response = chat(
        model=MODEL,
        messages=messages,
        think=False,
        stream=False,
    )

    response_text = response.message.content

    memory.add_message("assistant", response_text)

    return response_text