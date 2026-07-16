"""
utils/wikivoyage_client.py
-----------------------------
Thin client for the Wikivoyage API (en.wikivoyage.org). Wikivoyage is a
free, openly-licensed (CC BY-SA) travel wiki with detailed guides for
almost every city/region worldwide — off-beat spots, culture notes,
transport info, exactly the kind of texture your other tools don't
provide.

This is used two ways:
  1. scripts/build_vector_store.py — to PRE-LOAD a list of popular
     destinations into the vector store ahead of time.
  2. utils/rag_retriever.py — to fetch a destination LIVE, on demand, the
     first time someone asks about a place that isn't pre-loaded yet.
"""

import requests

WIKIVOYAGE_API_URL = "https://en.wikivoyage.org/w/api.php"


def fetch_wikivoyage_article(destination: str, timeout: int = 10) -> str | None:
    """
    Fetch the plain-text extract of a Wikivoyage article for the given
    destination. Returns None if no matching article exists.

    Uses `redirects=1` so e.g. "Bombay" resolves to the "Mumbai" article
    the same way the Wikivoyage website itself would.
    """
    params = {
        "action": "query",
        "titles": destination,
        "prop": "extracts",
        "explaintext": 1,
        "redirects": 1,
        "format": "json",
    }
    headers = {
        # Wikimedia asks for a descriptive User-Agent identifying the app.
        "User-Agent": "AiTripPlannerBot/1.0 (student project; contact via GitHub)"
    }

    try:
        response = requests.get(
            WIKIVOYAGE_API_URL, params=params, headers=headers, timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1" or "missing" in page:
            return None  # no matching article
        extract = page.get("extract", "").strip()
        return extract if extract else None

    return None