"""
bot.websearch  -  Google-style web search via DuckDuckGo
========================================================
Provides real-time web results (no API key required) so the assistant can
answer questions about current events and "search ..." commands.

Uses the `ddgs` package (falls back to the older `duckduckgo_search` name).
Returns plain data structures so the module stays easy to unit-test.
"""

from __future__ import annotations

from typing import List, TypedDict


class SearchHit(TypedDict):
    title: str
    body: str
    href: str


def web_search(query: str, max_results: int = 5) -> List[SearchHit]:
    """Return up to `max_results` web results, or [] if the search fails."""
    hits: List[SearchHit] = []
    try:
        try:
            from ddgs import DDGS            # current package name
        except ImportError:
            from duckduckgo_search import DDGS  # legacy package name
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                hits.append({
                    "title": r.get("title", ""),
                    "body": r.get("body", ""),
                    "href": r.get("href", ""),
                })
    except Exception as exc:
        print(f"[search] failed: {exc}")
    return hits


def format_context(hits: List[SearchHit]) -> str:
    """Render hits into a numbered block for grounding the LLM."""
    if not hits:
        return ""
    return "\n".join(
        f"{i}. {h['title']}\n   {h['body']}\n   {h['href']}"
        for i, h in enumerate(hits, 1)
    )


def format_sources(hits: List[SearchHit], limit: int = 3) -> str:
    """A short, human-readable list of source links for the terminal."""
    if not hits:
        return ""
    lines = [f"  - {h['title']}: {h['href']}" for h in hits[:limit] if h["href"]]
    return "Sources:\n" + "\n".join(lines) if lines else ""
