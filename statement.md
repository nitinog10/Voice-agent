# Problem Statement — Terminal Voice Assistant

## Problem Statement

People interact with their computers almost entirely through typing and
clicking. For quick, everyday actions — opening an application, looking
something up on the web, asking a factual question, getting help with a small
piece of code, or brainstorming an idea — switching between the keyboard, the
mouse, a browser, and different apps is slow and breaks concentration. Existing
commercial voice assistants (Alexa, Siri, Google Assistant) are closed,
cloud-locked, tied to specific hardware, and cannot be extended by a student or
inspected to learn *how* they work.

**This project builds an open, fully-Python, terminal-based voice assistant**
that a user can talk to. It listens to a spoken command, understands the
intent, performs the action (open an app, search the web, or reason with a
large language model), and speaks the answer back in a natural female voice —
all controlled from the terminal with a simple "press Enter to talk" turn.

## Scope of the Project

**In scope**
- A hands-light, voice-driven command loop that runs in any terminal.
- Speech-to-text capture from the microphone (7-second window to start speaking,
  ends automatically when the user pauses).
- Three functional modules: **Application Launcher**, **Web Search**, and an
  **AI Reasoning brain** (question answering, code help, brainstorming).
- Natural, female text-to-speech replies, with full/long answers (including
  code) also printed to the terminal for reading.
- Configuration through a single `.env` file (AWS keys, voice, timings).
- Graceful degradation: if the microphone is unavailable, the user can type;
  if a service is missing, the assistant explains instead of crashing.

**Out of scope**
- Graphical, web, or mobile interfaces (the project is intentionally Python-only,
  terminal-only).
- Messaging other people (e.g. WhatsApp) or any action that could reach a third
  party — deliberately excluded for safety and simplicity.
- Multi-user accounts, persistent databases, or cloud deployment.

## Target Users

- **Students and learners** who want a transparent, hackable example of how a
  voice assistant is built (speech I/O + intent routing + LLM).
- **Developers** who want a fast, keyboard-free way to open tools, search, and
  get quick coding help without leaving the terminal.
- **Accessibility-minded users** who prefer speaking and listening over typing
  and reading for short interactions.

## High-Level Features

1. **Voice command loop** — press Enter, speak, pause; the assistant acts, then
   waits for you to return to the terminal before listening again (so it never
   captures its own voice or background noise).
2. **Open applications & websites** — "open notepad", "open vs code",
   "open youtube", "open gmail", "open github", "open google".
3. **Web search** — "search latest AI news" / "google python tips" fetches live
   DuckDuckGo results and speaks a grounded summary, printing the source links.
4. **AI reasoning (AWS Bedrock / Amazon Nova)** — answers general questions,
   writes and explains code, and helps brainstorm; concise spoken summary plus a
   full on-screen answer.
5. **Natural female voice** — offline text-to-speech that reads clean,
   markdown-free replies.
6. **Safe & configurable** — no third-party messaging; all settings and secrets
   live in a git-ignored `.env` file.
