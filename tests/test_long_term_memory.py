from app.memory.long_term import LongTermMemory


def test_save_memory():
    memory = LongTermMemory()

    memory.save_memory(
        memory_type="test",
        memory_key="name",
        memory_value="Gowtham",
    )

    result = memory.get_memory("name")

    assert result == (
        "test",
        "name",
        "Gowtham",
    )

    memory.deactivate_memory(
        "test",
        "name",
    )

    memory.connection.close()
    
def test_update_memory():
    memory = LongTermMemory()

    memory.save_memory(
        memory_type="test",
        memory_key="city",
        memory_value="Hyderabad",
    )

    memory.save_memory(
        memory_type="test",
        memory_key="city",
        memory_value="Bengaluru",
    )

    result = memory.get_memory("city")

    assert result == (
        "test",
        "city",
        "Bengaluru",
    )

    memory.deactivate_memory(
        "test",
        "city",
    )

    memory.connection.close()
    
    
def test_deactivate_memory():
    memory = LongTermMemory()

    memory.save_memory(
        memory_type="test",
        memory_key="email",
        memory_value="test@example.com",
    )

    rows_updated = memory.deactivate_memory(
        "test",
        "email",
    )

    assert rows_updated == 1

    result = memory.get_memory("email")

    assert result is None

    memory.connection.close()
    
    
def test_reactivate_memory():
    memory = LongTermMemory()

    memory.save_memory(
        memory_type="test",
        memory_key="language",
        memory_value="Python",
    )

    memory.deactivate_memory(
        "test",
        "language",
    )

    assert memory.get_memory("language") is None

    memory.save_memory(
        memory_type="test",
        memory_key="language",
        memory_value="Java",
    )

    result = memory.get_memory("language")

    assert result == (
        "test",
        "language",
        "Java",
    )

    memory.connection.close()