from app.memory.context import build_memory_context


def test_build_memory_context():
    memories = [
        {
            "memory_type": "fact",
            "memory_key": "name",
            "memory_value": "Gowtham",
        },
        {
            "memory_type": "preference",
            "memory_key": "response_style",
            "memory_value": "concise explanations",
        },
    ]

    result = build_memory_context(memories)

    assert result == (
        "Known information about the user:\n"
        "- name: Gowtham\n"
        "- response_style: concise explanations"
    )


def test_empty_memories_return_empty_context():
    result = build_memory_context([])

    assert result == ""


def test_multiple_memories_are_preserved():
    memories = [
        {
            "memory_type": "fact",
            "memory_key": "name",
            "memory_value": "Gowtham",
        },
        {
            "memory_type": "fact",
            "memory_key": "location",
            "memory_value": "Hyderabad",
        },
        {
            "memory_type": "fact",
            "memory_key": "learning",
            "memory_value": "Machine Learning",
        },
    ]

    result = build_memory_context(memories)

    assert "- name: Gowtham" in result
    assert "- location: Hyderabad" in result
    assert "- learning: Machine Learning" in result