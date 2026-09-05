from ollama import chat
from app.memory.detector import detect_memory
from app.memory.conversation import ConversationMemory
from app.memory.long_term import LongTermMemory
from app.tools.router import route_tool


MODEL = "qwen3:8b"

SYSTEM_PROMPT = """
You are Leny, a local personal AI assistant.

Your name is Leny.
Be concise and useful.
"""


memory = ConversationMemory()
long_term_memory = LongTermMemory()


def remember_memory(
    memory_type: str,
    memory_key: str,
    memory_value: str,
):
    """
    Save a long-term memory for Leny.
    """

    long_term_memory.save_memory(
        memory_type=memory_type,
        memory_key=memory_key,
        memory_value=memory_value,
    )

    return "Memory saved successfully."


def recall_memory(memory_key: str):
    """
    Retrieve an active long-term memory for Leny.
    """

    return long_term_memory.get_memory(memory_key)


def ask_leny(message: str) -> str:
    tool_result = route_tool(message)

    if tool_result is not None:
        response_text = str(tool_result)

        memory.add_message("user", message)

        detected_memory = detect_memory(message)

        if detected_memory is not None:
            remember_memory(
            memory_type=detected_memory["memory_type"],
            memory_key=detected_memory["memory_key"],
            memory_value=detected_memory["memory_value"],
            )
        memory.add_message("assistant", response_text)

        return response_text

    memory.add_message("user", message)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # Retrieve known long-term memory.
    name_memory = recall_memory("name")

    if name_memory is not None:
        memory_context = (
            f"The user's name is {name_memory[2]}."
        )

        messages.append(
            {
                "role": "system",
                "content": memory_context,
            }
        )

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