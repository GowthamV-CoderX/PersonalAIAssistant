ALLOWED_MEMORY_TYPES = {
    "fact",
    "preference",
}

ALLOWED_MEMORY_KEYS = {
    "name",
    "location",
    "learning",
    "favorite_language",
    "response_style",
}

MAX_MEMORY_VALUE_LENGTH = 500


def validate_memory(memory: dict) -> bool:
    """
    Validate a memory before it is persisted.
    """

    if not isinstance(memory, dict):
        return False

    required_fields = {
        "memory_type",
        "memory_key",
        "memory_value",
    }

    if not required_fields.issubset(memory.keys()):
        return False

    memory_type = memory["memory_type"]
    memory_key = memory["memory_key"]
    memory_value = memory["memory_value"]

    if memory_type not in ALLOWED_MEMORY_TYPES:
        return False

    if memory_key not in ALLOWED_MEMORY_KEYS:
        return False

    if not isinstance(memory_value, str):
        return False

    memory_value = memory_value.strip()

    if not memory_value:
        return False

    if len(memory_value) > MAX_MEMORY_VALUE_LENGTH:
        return False

    return True