from app.memory.conversation import ConversationMemory


def test_memory_starts_empty():
    memory = ConversationMemory()

    assert memory.get_messages() == []


def test_add_message():
    memory = ConversationMemory()

    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi!")

    assert memory.get_messages() == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
    ]


def test_get_messages_returns_copy():
    memory = ConversationMemory()

    memory.add_message("user", "Hello")

    messages = memory.get_messages()
    messages.append(
        {
            "role": "assistant",
            "content": "Fake message",
        }
    )

    assert len(memory.get_messages()) == 1


def test_clear_memory():
    memory = ConversationMemory()

    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi!")

    memory.clear()

    assert memory.get_messages() == []
    
def test_memory_respects_max_messages():
    memory = ConversationMemory(max_messages=3)

    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Message 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Message 4")

    assert memory.get_messages() == [
        {"role": "assistant", "content": "Message 2"},
        {"role": "user", "content": "Message 3"},
        {"role": "assistant", "content": "Message 4"},
    ]