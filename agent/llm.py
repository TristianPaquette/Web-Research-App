"""
llm.py - wraps the Anthropic API to answer a question given web context.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# The Anthropic SDK automatically reads ANTHROPIC_API_KEY from .env
client = Anthropic()

MODEL = "claude-opus-4-7"

SYSTEM_PROMPT = """You are a careful research assistant. You will be given a user's
question along with teh text of several web pages that were retrieved from a web search.
Your job is to write a clear, concices answer to the question using ONLY the information
in the provided pages.

Rules:
- If the page don't contain the answer, Say so, Do not guess.
- Cite the sources you used inline using bracket numbers like [1], [2].
- Keep the answer focused. Two to four short paragraphs is usually enough.
- End with a "Sources:" section listing the URLs you cited.
"""

def answer_question(question: str, pages: list[dict]) -> str:
    """
    pages: a list of {"title": ..., "url": ..., "text": ...} dicts.
    Returns Claude's written answer as a string.
    """

    # Build the context block. Each page gets numbered so Claude can cite it.
    context_parts = []
    for i, page in enumerate(pages, start=1):
        context_parts.append(
            f"[{i}] {page['title']}\nURL: {page['url']}\n{page['text']}\n"
        )
    context = "\n---\n".join(context_parts)

    user_message = (
        f"Question: {question}\n\n"
        f"Here are the web pages I found: \n\n{context}\n\n"
        f"Please answer the question using these sources."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens = 1024,
        system = SYSTEM_PROMPT,
        messages = [{"role": "user", "content": user_message}],
    )

    # response.content is a list of blocks: the first one's text is the answer.
    return response.content[0].text

# Quick test
if __name__ == "__main__":
    fake_pages = [{
        "title": "Python (programming language) - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "text": "Python is a high-level, general-purpose programming language."
                "Its design philosophy emphasizes code readability with the use "
                "of significant indentation. Python was created by Guido van Rossum "
                "and first released in 1991."
    }]
    print(answer_question("Who created Python?", fake_pages))