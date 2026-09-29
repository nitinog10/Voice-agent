#!/usr/bin/env python3
"""
Terminal Voice Assistant  -  entry point.

A Python-only, voice-controlled assistant that runs entirely in your terminal.
Press Enter, speak a command, and it will open apps, search the web, or answer
questions (including coding help and brainstorming) using AWS Bedrock.

Run:
    venv\\Scripts\\python.exe voicebot.py     (Windows)
    python voicebot.py                        (macOS / Linux)

All the logic lives in the `bot` package; this file just starts the session.
"""

from bot.session import VoiceSession


def main() -> None:
    VoiceSession().run()


if __name__ == "__main__":
    main()
