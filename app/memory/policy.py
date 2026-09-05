import re


def should_store_memory(message: str) -> bool:
    """
    Decide whether a user message contains information
    that should be considered for long-term memory.
    """

    message = message.strip()

    if not message:
        return False

    memory_patterns = [
        r"^my name is .+$",
        r"^i live in .+$",
        r"^i am learning .+$",
        r"^remember that .+$",
        r"^remember .+$",
        r"^my favorite .+ is .+$",
        r"^i prefer .+$",
    ]

    for pattern in memory_patterns:
        if re.fullmatch(pattern, message, re.IGNORECASE):
            return True

    return False