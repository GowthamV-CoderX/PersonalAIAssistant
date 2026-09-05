import re


def detect_memory(message: str):
    """
    Detect simple user facts that are worth storing
    as long-term memory.
    """

    patterns = [
        (
            r"my name is (.+)",
            "name",
        ),
        (
            r"i live in (.+)",
            "location",
        ),
        (
            r"i am learning (.+)",
            "learning",
        ),
    ]

    message = message.strip()

    for pattern, memory_key in patterns:
        match = re.fullmatch(
            pattern,
            message,
            re.IGNORECASE,
        )

        if match:
            value = match.group(1).strip()

            return {
                "memory_type": "fact",
                "memory_key": memory_key,
                "memory_value": value,
            }

    return None