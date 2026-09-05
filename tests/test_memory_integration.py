from app.memory.detector import detect_memory
from app.memory.policy import should_store_memory
from app.memory.validator import validate_memory


def test_memory_pipeline_accepts_valid_memory():
    message = "My name is Gowtham"

    assert should_store_memory(message) is True

    memory = detect_memory(message)

    assert memory is not None
    assert validate_memory(memory) is True


def test_memory_pipeline_accepts_explicit_memory():
    message = "Remember that I prefer concise explanations"

    assert should_store_memory(message) is True

    memory = detect_memory(message)

    assert memory == {
        "memory_type": "preference",
        "memory_key": "response_style",
        "memory_value": "concise explanations",
    }

    assert validate_memory(memory) is True


def test_memory_pipeline_rejects_normal_message():
    message = "What is machine learning?"

    assert should_store_memory(message) is False

    memory = detect_memory(message)

    assert memory is None


def test_memory_pipeline_rejects_calculation():
    message = "Calculate 847 * 293"

    assert should_store_memory(message) is False

    memory = detect_memory(message)

    assert memory is None
    
    
import os

import mysql.connector
from dotenv import load_dotenv

from app.memory.long_term import LongTermMemory


load_dotenv()


def test_memory_conflict_lifecycle():
    memory = LongTermMemory()

    test_key = "integration_test_language"

    try:
        # Start clean.
        memory.deactivate_memory(
            "preference",
            test_key,
        )

        # First value.
        result = memory.save_memory_with_conflict_resolution(
            memory_type="preference",
            memory_key=test_key,
            memory_value="Python",
        )

        assert result == "created"

        # Conflicting value.
        result = memory.save_memory_with_conflict_resolution(
            memory_type="preference",
            memory_key=test_key,
            memory_value="Java",
        )

        assert result == "updated"

        # Verify only Java is active.
        cursor = memory.connection.cursor()

        cursor.execute(
            """
            SELECT memory_value, is_active
            FROM memories
            WHERE memory_type = %s
              AND memory_key = %s
            ORDER BY id
            """,
            ("preference", test_key),
        )

        rows = cursor.fetchall()

        cursor.close()

        assert rows == [
            ("Python", 0),
            ("Java", 1),
        ]

    finally:
        memory.deactivate_memory(
            "preference",
            test_key,
        )

        memory.connection.close()