from app.memory.detector import detect_memory


def test_detect_name():
    result = detect_memory("My name is Gowtham")

    assert result == {
        "memory_type": "fact",
        "memory_key": "name",
        "memory_value": "Gowtham",
    }


def test_detect_location():
    result = detect_memory("I live in Hyderabad")

    assert result == {
        "memory_type": "fact",
        "memory_key": "location",
        "memory_value": "Hyderabad",
    }


def test_detect_learning():
    result = detect_memory("I am learning machine learning")

    assert result == {
        "memory_type": "fact",
        "memory_key": "learning",
        "memory_value": "machine learning",
    }


def test_ignore_normal_message():
    result = detect_memory("What is machine learning?")

    assert result is None