MEMORY_KEYWORDS = {
    "name": {
        "name",
        "called",
    },
    "location": {
        "location",
        "live",
        "city",
    },
    "learning": {
        "learning",
        "learn",
        "studying",
        "study",
    },
    "favorite_language": {
        "language",
        "programming",
        "code",
    },
    "response_style": {
        "concise",
        "detailed",
        "explain",
        "explanation",
        "response",
    },
}



import re


def _tokenize(text: str) -> set[str]:
    """
    Convert text into normalized word tokens.
    """

    return set(
        re.findall(
            r"\b[a-zA-Z_]+\b",
            text.lower(),
        )
    )


def score_memory(message: str, memory: dict) -> int:
    """
    Calculate a deterministic relevance score for a memory.
    """

    message_tokens = _tokenize(message)

    memory_key = memory["memory_key"]
    memory_value = memory["memory_value"]

    keywords = MEMORY_KEYWORDS.get(
        memory_key,
        set(),
    )

    score = 0

    if memory_key.lower() in message_tokens:
        score += 2

    keyword_matches = message_tokens.intersection(
        keywords
    )

    score += len(keyword_matches)

    value_tokens = _tokenize(memory_value)

    value_matches = message_tokens.intersection(
        value_tokens
    )

    score += len(value_matches)

    return score


def retrieve_relevant_memories(
    message: str,
    memories: list[dict],
    min_score: int = 1,
) -> list[dict]:
    """
    Retrieve memories relevant to the user's message.
    """

    scored_memories = []

    for memory in memories:
        score = score_memory(
            message,
            memory,
        )

        if score >= min_score:
            scored_memories.append(
                (score, memory)
            )

    scored_memories.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        memory
        for score, memory in scored_memories
    ]