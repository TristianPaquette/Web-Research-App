"""
scraper.py - fetches a URL and extracts teh clean readable text.
"""

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh: Intel Mac OS X 10_15_7)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/120.0 Safari/537.36"
    )
}

def fetch_page_text(url: str, max_chars: int = 5000) -> str:
    """Download a page and return its readable text (truncated)."""
    try:
        response = requests.get(url, headers=HEADERS, timeout = 15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f" [skip] couldn't fetch {url}: {e}")
        return ""
    
    # Parse the HTML into a tree of node we can walk.
    soup = BeautifulSoup(response.text, "html.parser")

    # Throw away parts of the page that aren't readable content.
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()

    # joins all remaining text with spaces.
    text = soup.get_text(separator=" ", strip=True)

    # Collapse runs of whitespace
    text = " ".join(text.split())

    return text[:max_chars]

# Quick test
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    text = fetch_page_text(url)
    print(text[:500], "...")

