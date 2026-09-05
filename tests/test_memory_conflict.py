from unittest.mock import MagicMock

from app.memory.long_term import LongTermMemory


def create_memory_service():
    service = LongTermMemory.__new__(LongTermMemory)

    service.connection = MagicMock()

    return service


def test_new_memory_is_created():
    service = create_memory_service()

    cursor = service.connection.cursor.return_value
    cursor.fetchone.return_value = None

    result = service.save_memory_with_conflict_resolution(
        memory_type="preference",
        memory_key="favorite_language",
        memory_value="Python",
    )

    assert result == "created"

    service.connection.commit.assert_called_once()


def test_same_memory_is_unchanged():
    service = create_memory_service()

    cursor = service.connection.cursor.return_value
    cursor.fetchone.return_value = (10, "Python")

    result = service.save_memory_with_conflict_resolution(
        memory_type="preference",
        memory_key="favorite_language",
        memory_value="Python",
    )

    assert result == "unchanged"

    service.connection.commit.assert_not_called()


def test_conflicting_memory_is_updated():
    service = create_memory_service()

    cursor = service.connection.cursor.return_value
    cursor.fetchone.return_value = (10, "Python")

    result = service.save_memory_with_conflict_resolution(
        memory_type="preference",
        memory_key="favorite_language",
        memory_value="Java",
    )

    assert result == "updated"

    service.connection.commit.assert_called_once()

    assert cursor.execute.call_count == 3