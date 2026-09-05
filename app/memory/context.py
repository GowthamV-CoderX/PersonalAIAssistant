def build_memory_context(memories: list[dict]) -> str:
    """
    Convert structured memories into concise LLM context.
    """

    if not memories:
        return ""

    lines = ["Known information about the user:"]

    for memory in memories:
        lines.append(
            f"- {memory['memory_key']}: "
            f"{memory['memory_value']}"
        )

    return "\n".join(lines)