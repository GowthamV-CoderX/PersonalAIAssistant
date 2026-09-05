from ollama import chat


MODEL = "qwen3:8b"

SYSTEM_PROMPT = """
You are Leny, a local personal AI assistant.

Your name is Leny.
Do not identify yourself as Qwen unless the user specifically asks which underlying model you use.

Be concise and useful.
For simple questions, answer directly without unnecessary reasoning.
"""


def ask_leny(message: str) -> str:
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        think=False,
        stream=True,
    )

    full_response = ""

    for chunk in response:
        content = chunk.message.content

        if content:
            print(content, end="", flush=True)
            full_response += content

    print()

    return full_response