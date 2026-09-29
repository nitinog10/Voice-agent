"""
bot.apps  -  Application & website launcher
===========================================
Opens desktop applications and popular websites in response to spoken
"open ..." commands, e.g. "open notepad", "open youtube", "open vs code".

Websites open in the default browser; desktop apps launch as subprocesses.
Every launch is wrapped in error handling so a missing app never crashes the
assistant - it just reports what went wrong.
"""

from __future__ import annotations

import platform
import subprocess
import webbrowser

# name -> URL for common websites the user asked for.
SITES = {
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "linkedin": "https://www.linkedin.com",
    "github": "https://github.com",
    "google": "https://www.google.com",
    "slack": "https://app.slack.com",
}

# Spoken keyword(s) -> local executable for desktop apps.
DESKTOP_APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "vs code": "code",
    "vscode": "code",
    "visual studio code": "code",
    "command prompt": ["cmd.exe"],
    "explorer": ["explorer.exe"],
}


def _launch(cmd) -> bool:
    try:
        subprocess.Popen(cmd, shell=isinstance(cmd, str))
        return True
    except Exception:
        return False


def open_target(text: str) -> str:
    """Open the app or site named in `text`. Returns a spoken confirmation."""
    t = text.lower()

    # Desktop applications first (more specific keywords).
    for keyword, cmd in DESKTOP_APPS.items():
        if keyword in t:
            nice = keyword.title()
            if keyword == "slack":  # handled below as site fallback too
                break
            return f"Opening {nice}." if _launch(cmd) else \
                   f"I couldn't open {nice}. Is it installed and on your PATH?"

    # Slack: try the desktop app, then fall back to the web app.
    if "slack" in t:
        if platform.system() == "Windows" and _launch("slack"):
            return "Opening Slack."
        webbrowser.open(SITES["slack"])
        return "Opening Slack in your browser."

    # Websites.
    for name, url in SITES.items():
        if name in t:
            webbrowser.open(url)
            return f"Opening {name.title()}."

    return ""  # nothing matched -> let the router try other intents
