from app.memory.policy import should_store_memory


def test_store_name():
    assert should_store_memory("My name is Gowtham") is True


def test_store_location():
    assert should_store_memory("I live in Hyderabad") is True


def test_store_learning():
    assert should_store_memory("I am learning machine learning") is True


def test_store_explicit_memory_request():
    assert should_store_memory(
        "Remember that I prefer concise explanations"
    ) is True


def test_store_preference():
    assert should_store_memory(
        "I prefer concise explanations"
    ) is True


def test_store_favorite():
    assert should_store_memory(
        "My favorite language is Python"
    ) is True


def test_ignore_question():
    assert should_store_memory(
        "What is machine learning?"
    ) is False


def test_ignore_calculation():
    assert should_store_memory(
        "Calculate 847 * 293"
    ) is False


def test_ignore_temporary_information():
    assert should_store_memory(
        "I ate biryani today"
    ) is False


def test_ignore_empty_message():
    assert should_store_memory("") is False