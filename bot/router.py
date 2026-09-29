"""
bot.router  -  Intent detection & command routing
==================================================
The router is the decision-making core: it takes one line of recognised text,
figures out *what the user wants* (the intent), performs the matching action,
and returns a `Reply`.

A `Reply` separates what is shown on screen (`text`, which may include code)
from what is spoken aloud (`speech`, always clean and concise). This keeps the
voice output pleasant even when the on-screen answer contains code blocks.

Intents, in priority order:
  1. exit         - "exit" / "quit" / "goodbye"
  2. open         - "open <app or site>"
  3. search       - "search ..." / "google ..." -> web search, grounded answer
  4. ask (default)- any other query -> LLM (Q&A, coding help, brainstorming)
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from . import apps
from .llm import Brain
from .tts import clean_for_speech
from .websearch import web_search, format_context, format_sources

EXIT_WORDS = ("exit", "quit", "goodbye", "good bye", "stop listening", "bye bye")
_SEARCH_RE = re.compile(r"^(search(?:\s+for)?|google|look\s+up|find)\s+(.*)$", re.I)
_OPEN_HINTS = list(apps.SITES) + list(apps.DESKTOP_APPS)


@dataclass
class Reply:
    text: str          # full answer for the terminal (may include code)
    speech: str        # concise, clean text for the voice
    should_exit: bool = False


def _spoken_summary(full: str) -> str:
    """Make a voice-friendly version of a possibly-long, code-containing answer."""
    has_code = "```" in full
    spoken = clean_for_speech(full)
    if has_code:
        lead = spoken.split(". ")[0] if spoken else "Here's what I found"
        return f"{lead}. I've printed the full answer with the code in your terminal."
    if len(spoken) > 700:  # very long prose -> speak the first part
        return spoken[:700].rsplit(". ", 1)[0] + ". The full answer is in your terminal."
    return spoken


class CommandRouter:
    """Routes a recognised command to the right action and returns a Reply."""

    def __init__(self, brain: Brain | None = None) -> None:
        self.brain = brain or Brain()

    def route(self, text: str) -> Reply:
        if not text:
            return Reply("I didn't catch that. Please say it again.",
                        "I didn't catch that. Please say it again.")

        # 1. Exit
        if any(w in text for w in EXIT_WORDS):
            return Reply("Goodbye!", "Goodbye!", should_exit=True)

        # 2. Explicit web search  ("search ...", "google ...", "look up ...")
        #    Checked before "open" so "google python tips" searches, not opens.
        m = _SEARCH_RE.match(text)
        if m:
            return self._search(m.group(2).strip())

        # 3. Open an app or website ("open ...", "launch ...", or a bare app name)
        if self._is_open_command(text):
            result = apps.open_target(text)
            if result:
                return Reply(result, result)

        # 4. Default: ask the LLM (general Q&A, coding, brainstorming)
        full = self.brain.answer(text)
        return Reply(full, _spoken_summary(full))

    @staticmethod
    def _is_open_command(text: str) -> bool:
        """True only for real 'open' intents, not any sentence mentioning a site."""
        if text.startswith(("open", "launch", "go to", "start ")):
            return True
        first = text.split(maxsplit=1)[0] if text else ""
        return first in _OPEN_HINTS

    def _search(self, query: str) -> Reply:
        if not query:
            return Reply("What would you like me to search for?",
                        "What would you like me to search for?")
        # Open Google in the browser with the query already searched.
        apps.google_search(query)
        # Also fetch results so we can speak a short grounded summary.
        hits = web_search(query)
        if not hits:
            msg = f"I've opened Google and searched for {query}."
            return Reply(msg, msg)
        context = format_context(hits)
        answer = self.brain.answer(
            f"Summarise the web results for '{query}':\n{context}",
            ground_with_search=False,
        )
        sources = format_sources(hits)
        full = (f"Opened Google for '{query}'.\n\n{answer}"
                + (f"\n\n{sources}" if sources else ""))
        spoken = f"I've opened Google for {query}. {_spoken_summary(answer)}"
        return Reply(full, spoken)
