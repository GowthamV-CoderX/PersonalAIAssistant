from unittest.mock import MagicMock

from app.memory.long_term import LongTermMemory


def create_memory_service():
    service = LongTermMemory.__new__(LongTermMemory)

    service.connection = MagicMock()

    return service


def test_get_active_memories_returns_structured_memories():
    service = create_memory_service()

    cursor = service.connection.cursor.return_value

    cursor.fetchall.return_value = [
        ("fact", "name", "Gowtham"),
        (
            "preference",
            "response_style",
            "concise explanations",
        ),
    ]

    result = service.get_active_memories()

    assert result == [
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


def test_get_active_memories_returns_empty_list_when_no_memories():
    service = create_memory_service()

    cursor = service.connection.cursor.return_value

    cursor.fetchall.return_value = []

    result = service.get_active_memories()

    assert result == []


def test_get_active_memories_executes_query():
    service = create_memory_service()

    cursor = service.connection.cursor.return_value
    cursor.fetchall.return_value = []

    service.get_active_memories()

    cursor.execute.assert_called_once()

    query = cursor.execute.call_args[0][0]

    assert "is_active = TRUE" in query
    
    
from app.memory.retrieval import (
    retrieve_relevant_memories,
    score_memory,
)


def test_score_memory_matches_key():
    memory = {
        "memory_type": "fact",
        "memory_key": "name",
        "memory_value": "Gowtham",
    }

    score = score_memory(
        "What is my name?",
        memory,
    )

    assert score >= 2


def test_retrieve_relevant_memory():
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
    ]

    result = retrieve_relevant_memories(
        "What is my name?",
        memories,
    )

    assert result == [memories[0]]


def test_retrieve_learning_memory():
    memories = [
        {
            "memory_type": "fact",
            "memory_key": "learning",
            "memory_value": "Machine Learning",
        },
        {
            "memory_type": "fact",
            "memory_key": "location",
            "memory_value": "Hyderabad",
        },
    ]

    result = retrieve_relevant_memories(
        "What am I learning?",
        memories,
    )

    assert result == [memories[0]]


def test_irrelevant_memories_are_excluded():
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
    ]

    result = retrieve_relevant_memories(
        "What is the weather today?",
        memories,
    )

    assert result == []


def test_memories_are_sorted_by_relevance():
    memories = [
        {
            "memory_type": "fact",
            "memory_key": "name",
            "memory_value": "Gowtham",
        },
        {
            "memory_type": "preference",
            "memory_key": "favorite_language",
            "memory_value": "Python",
        },
    ]

    result = retrieve_relevant_memories(
        "What programming language do I like?",
        memories,
    )

    assert result[0]["memory_key"] == "favorite_language"