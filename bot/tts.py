"""
bot.tts  -  Text-to-Speech (the assistant's voice)
==================================================
Wraps pyttsx3 (offline Windows SAPI5 engine) and selects a **female** voice.

A fresh engine is created for every utterance: pyttsx3's run-loop can dead-lock
if a single engine instance is reused across many `runAndWait()` calls, so a
short-lived engine per line is the most reliable pattern on Windows.
"""

from __future__ import annotations

import re

from .config import config

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

# Common Windows voice names, split by gender, used to pick a voice.
_FEMALE_HINTS = ("zira", "hazel", "heera", "aria", "eva", "susan", "female")
_MALE_HINTS = ("david", "mark", "george", "ravi", "male")


def clean_for_speech(text: str) -> str:
    """Strip markdown and code so the reply reads aloud cleanly."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)   # drop fenced code blocks
    text = re.sub(r"`([^`]*)`", r"\1", text)              # inline code -> plain
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)        # [label](url) -> label
    text = re.sub(r"[*_#>|~]+", "", text)                  # markdown symbols
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _select_voice(engine) -> None:
    """Apply a female (or male) SAPI voice based on config.voice_gender."""
    try:
        voices = engine.getProperty("voices")
    except Exception:
        return
    hints = _FEMALE_HINTS if config.voice_gender == "female" else _MALE_HINTS
    for v in voices:
        meta = f"{getattr(v, 'name', '')} {getattr(v, 'id', '')}".lower()
        gender = str(getattr(v, "gender", "")).lower()
        if any(h in meta for h in hints) or config.voice_gender in gender:
            engine.setProperty("voice", v.id)
            return


class Speaker:
    """Speaks text aloud with a female voice, and echoes it to the terminal."""

    def __init__(self) -> None:
        self.available = pyttsx3 is not None

    def say(self, text: str) -> None:
        print(f"\n\033[92m[assistant]\033[0m {text}\n")
        if not self.available:
            return
        spoken = clean_for_speech(text)
        if not spoken:
            return
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", config.speech_rate)
            _select_voice(engine)
            engine.say(spoken)
            engine.runAndWait()
            engine.stop()
        except Exception as exc:
            print(f"[tts] could not speak: {exc}")
