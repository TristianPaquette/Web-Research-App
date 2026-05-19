"""
search.py - wraps the Tavily search API

Given a question, returns a list of dicts:
[{"title": ..., "url": ..., "content": ...}, ...]
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Read .env from the same folder as this file
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise RuntimeError("Missing TAVILY_API_KEY. Make sure it is in your .env file.")

TAVILY_URL = "https://api.tavily.com/search"


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Search the web using the Tavily API and return a list of result dicts."""

    payload = {
        "query": query,
        "max_results": max_results,
        "search_depth": "basic",  # basic is fast and cheaper
        "include_answer": False,  # we will generate our own answer using Claude
    }

    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(TAVILY_URL, json=payload, headers=headers, timeout=30)

    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


# Quick test
if __name__ == "__main__":
    results = search_web("Who won the most recent Super Bowl?")
    for r in results:
        print(r["title"], "-", r["url"])