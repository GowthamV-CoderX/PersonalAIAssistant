import re


def detect_memory(message: str):
    """
    Detect and extract simple user facts that are worth storing
    as long-term memory.
    """

    message = message.strip()
    
    explicit_match = re.fullmatch(
    r"remember that (.+)",
    message,
    re.IGNORECASE,
    )

    if explicit_match:
        remembered_message = explicit_match.group(1).strip()

        detected_memory = detect_memory(
            remembered_message
        )

        if detected_memory is not None:
            return detected_memory

    patterns = [
        (
            r"my name is (.+)",
            "fact",
            "name",
        ),
        (
            r"i live in (.+)",
            "fact",
            "location",
        ),
        (
            r"i am learning (.+)",
            "fact",
            "learning",
        ),
        (
            r"my favorite language is (.+)",
            "preference",
            "favorite_language",
        ),
        (
            r"i prefer (.+)",
            "preference",
            "response_style",
        ),
    ]

    for pattern, memory_type, memory_key in patterns:
        match = re.fullmatch(
            pattern,
            message,
            re.IGNORECASE,
        )

        if match:
            value = match.group(1).strip()

            return {
                "memory_type": memory_type,
                "memory_key": memory_key,
                "memory_value": value,
            }

    return None