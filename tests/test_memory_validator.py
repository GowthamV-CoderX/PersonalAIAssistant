from app.memory.validator import validate_memory


def test_valid_fact_memory():
    memory = {
        "memory_type": "fact",
        "memory_key": "name",
        "memory_value": "Gowtham",
    }

    assert validate_memory(memory) is True


def test_valid_preference_memory():
    memory = {
        "memory_type": "preference",
        "memory_key": "response_style",
        "memory_value": "concise explanations",
    }

    assert validate_memory(memory) is True


def test_reject_non_dictionary():
    assert validate_memory("invalid") is False


def test_reject_missing_field():
    memory = {
        "memory_type": "fact",
        "memory_key": "name",
    }

    assert validate_memory(memory) is False


def test_reject_invalid_memory_type():
    memory = {
        "memory_type": "random",
        "memory_key": "name",
        "memory_value": "Gowtham",
    }

    assert validate_memory(memory) is False


def test_reject_invalid_memory_key():
    memory = {
        "memory_type": "fact",
        "memory_key": "random_key",
        "memory_value": "Gowtham",
    }

    assert validate_memory(memory) is False


def test_reject_non_string_value():
    memory = {
        "memory_type": "fact",
        "memory_key": "name",
        "memory_value": 123,
    }

    assert validate_memory(memory) is False


def test_reject_empty_value():
    memory = {
        "memory_type": "fact",
        "memory_key": "name",
        "memory_value": "   ",
    }

    assert validate_memory(memory) is False


def test_reject_excessively_long_value():
    memory = {
        "memory_type": "fact",
        "memory_key": "name",
        "memory_value": "a" * 501,
    }

    assert validate_memory(memory) is False