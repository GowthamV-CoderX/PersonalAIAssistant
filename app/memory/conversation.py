class ConversationMemory:
    """
    Stores the recent conversation history for Leny.
    """

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def get_messages(self) -> list[dict]:
        return self.messages.copy()

    def clear(self):
        self.messages.clear()