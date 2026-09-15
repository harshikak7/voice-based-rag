import requests

from app.config import (
    OLLAMA_URL,
    LLM_MODEL
)


def generate_answer(
    question: str,
    context: str
) -> str:

    prompt = f"""
You are a helpful Voice RAG assistant.

Answer the user's question using ONLY the
information provided in the context.

Do not use outside knowledge.

Do not invent facts.

If the answer cannot be found in the context,
say:

"I could not find that information in the uploaded documents."

Keep the answer:

- natural
- concise
- accurate
- easy to understand
- suitable for speaking aloud

==============================
CONTEXT
==============================

{context}

==============================
USER QUESTION
==============================

{question}

==============================
ANSWER
==============================
"""


    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }


    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=180
    )


    response.raise_for_status()


    data = response.json()


    answer = data.get(
        "response",
        ""
    ).strip()


    if not answer:

        return (
            "I could not generate an answer."
        )


    return answer