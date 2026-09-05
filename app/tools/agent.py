from ollama import chat
from app.memory.retrieval import retrieve_relevant_memories
from app.memory.detector import detect_memory
from app.memory.conversation import ConversationMemory
from app.memory.long_term import LongTermMemory
from app.memory.policy import should_store_memory
from app.tools.router import route_tool
from app.memory.validator import validate_memory
from app.memory.context import build_memory_context
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

    long_term_memory.save_memory_with_conflict_resolution(
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
        memory.add_message("assistant", response_text)

        return response_text

    memory.add_message("user", message)

    if should_store_memory(message):
        detected_memory = detect_memory(message)

        if detected_memory is not None:
            if validate_memory(detected_memory):
                remember_memory(
                    memory_type=detected_memory["memory_type"],
                    memory_key=detected_memory["memory_key"],
                    memory_value=detected_memory["memory_value"],
                )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    active_memories = long_term_memory.get_active_memories()

    relevant_memories = retrieve_relevant_memories(
        message,
        active_memories,
    )

    memory_context = build_memory_context(
        relevant_memories
    )

    if memory_context:
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