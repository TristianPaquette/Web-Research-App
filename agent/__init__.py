"""
agent package - connects search.py, scraper.py, and llm.py into one research() function.
"""

from .search import search_web
from .scraper import fetch_page_text
from .llm import answer_question


def research(question: str) -> dict:
    """
    Run the full agent:
    1. Search the web
    2. Fetch readable text from each result
    3. Ask Claude to answer using those pages

    Returns:
    {
        "answer": "...",
        "sources": [{"title": "...", "url": "..."}]
    }
    """

    # 1. Search the web
    results = search_web(question, max_results=5)

    # 2. Scrape each result and build the pages list for llm.py
    pages = []
    sources = []

    for result in results:
        title = result.get("title", "Untitled source")
        url = result.get("url")

        if not url:
            continue

        text = fetch_page_text(url)

        # If scraping fails, use Tavily's short content snippet as backup
        if not text:
            text = result.get("content", "")

        if not text:
            continue

        pages.append({
            "title": title,
            "url": url,
            "text": text,
        })

        sources.append({
            "title": title,
            "url": url,
        })

    if not pages:
        return {
            "answer": "I couldn't fetch readable text from any of the search results.",
            "sources": [],
        }

    # 3. Ask Claude to answer using the pages
    answer = answer_question(question, pages)

    return {
        "answer": answer,
        "sources": sources,
    }