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


def test_detect_favorite_language():
    result = detect_memory(
        "My favorite language is Python"
    )

    assert result == {
        "memory_type": "preference",
        "memory_key": "favorite_language",
        "memory_value": "Python",
    }


def test_detect_response_preference():
    result = detect_memory(
        "I prefer concise explanations"
    )

    assert result == {
        "memory_type": "preference",
        "memory_key": "response_style",
        "memory_value": "concise explanations",
    }


def test_ignore_normal_message():
    result = detect_memory(
        "What is machine learning?"
    )

    assert result is None


def test_ignore_calculation():
    result = detect_memory(
        "What is 10 * 5?"
    )

    assert result is None
    
def test_detect_explicit_memory_request():
    result = detect_memory(
        "Remember that I prefer concise explanations"
    )

    assert result == {
        "memory_type": "preference",
        "memory_key": "response_style",
        "memory_value": "concise explanations",
    }