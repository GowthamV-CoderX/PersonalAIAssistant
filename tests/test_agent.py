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