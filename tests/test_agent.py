from app.tools import agent


def test_agent_remembers_conversation(monkeypatch):
    agent.memory.clear()

    class FakeMessage:
        content = "Your name is Gowtham."

    class FakeResponse:
        message = FakeMessage()

    def fake_chat(**kwargs):
        messages = kwargs["messages"]

        assert messages[-1]["role"] == "user"
        assert messages[-1]["content"] == "What is my name?"

        return FakeResponse()

    agent.memory.add_message("user", "My name is Gowtham.")

    monkeypatch.setattr(agent, "chat", fake_chat)

    response = agent.ask_leny("What is my name?")

    assert response == "Your name is Gowtham."


def test_agent_stores_response(monkeypatch):
    agent.memory.clear()

    class FakeMessage:
        content = "Hello!"

    class FakeResponse:
        message = FakeMessage()

    def fake_chat(**kwargs):
        return FakeResponse()

    monkeypatch.setattr(agent, "chat", fake_chat)

    agent.ask_leny("Hello")

    messages = agent.memory.get_messages()

    assert messages[0] == {
        "role": "user",
        "content": "Hello",
    }

    assert messages[1] == {
        "role": "assistant",
        "content": "Hello!",
    }


def test_calculator_result_is_stored():
    agent.memory.clear()

    result = agent.ask_leny("What is 10 * 5?")

    assert result == "50"

    messages = agent.memory.get_messages()

    assert messages[-2] == {
        "role": "user",
        "content": "What is 10 * 5?",
    }

    assert messages[-1] == {
        "role": "assistant",
        "content": "50",
    }

def test_agent_injects_long_term_memory(monkeypatch):
    agent.memory.clear()

    class FakeMessage:
        content = "Your name is Gowtham."

    class FakeResponse:
        message = FakeMessage()

    def fake_chat(**kwargs):
        messages = kwargs["messages"]

        memory_message = next(
            message
            for message in messages
            if message["role"] == "system"
            and "Known information about the user:" in message["content"]
        )

        assert "- name: Gowtham" in memory_message["content"]

        return FakeResponse()

    monkeypatch.setattr(agent, "chat", fake_chat)

    monkeypatch.setattr(
        agent.long_term_memory,
        "get_active_memories",
        lambda: [
            {
                "memory_type": "fact",
                "memory_key": "name",
                "memory_value": "Gowtham",
            }
        ],
    )

    response = agent.ask_leny("What is my name?")

    assert response == "Your name is Gowtham."
    
    
    
def test_agent_injects_only_relevant_memories(monkeypatch):
    agent.memory.clear()

    class FakeMessage:
        content = "Your name is Gowtham."

    class FakeResponse:
        message = FakeMessage()

    def fake_chat(**kwargs):
        messages = kwargs["messages"]

        memory_messages = [
            message["content"]
            for message in messages
            if (
                message["role"] == "system"
                and "Known information about the user:" in message["content"]
            )
        ]

        assert len(memory_messages) == 1

        memory_context = memory_messages[0]

        assert "- name: Gowtham" in memory_context
        assert "Hyderabad" not in memory_context

        return FakeResponse()

    monkeypatch.setattr(agent, "chat", fake_chat)

    monkeypatch.setattr(
        agent.long_term_memory,
        "get_active_memories",
        lambda: [
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
        ],
    )

    response = agent.ask_leny("What is my name?")

    assert response == "Your name is Gowtham."
    
def test_agent_updates_conflicting_memory(monkeypatch):
    agent.memory.clear()

    class FakeMessage:
        content = "Memory updated."

    class FakeResponse:
        message = FakeMessage()

    def fake_chat(**kwargs):
        return FakeResponse()

    monkeypatch.setattr(agent, "chat", fake_chat)

    monkeypatch.setattr(
        agent.long_term_memory,
        "save_memory_with_conflict_resolution",
        lambda **kwargs: "updated",
    )

    response = agent.ask_leny(
        "My favorite language is Java"
    )

    assert response == "Memory updated."