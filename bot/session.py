"""
bot.session  -  The interactive voice session (main loop)
=========================================================
Ties every module together into the tap-to-talk experience:

    press Enter  ->  listen (up to 7s to start, until you pause)
                 ->  understand & act (router)
                 ->  speak the reply
                 ->  return to the prompt (does NOT auto-listen)

The assistant only listens again once you are "back on the terminal" and press
Enter. This prevents it from capturing its own spoken reply or background noise
as the next command. You may also just type a command instead of speaking.
"""

from __future__ import annotations

from .config import config
from .router import CommandRouter
from .stt import Listener
from .tts import Speaker

BANNER = r"""
==================================================================
              TERMINAL VOICE ASSISTANT  (Python)
   Brain: AWS Bedrock / Amazon Nova     Voice: female (offline)
------------------------------------------------------------------
  Press ENTER to talk. Then, after the beep-free 'listening' line,
  speak your command and pause - the assistant will act.
  Examples:
     "open youtube"        "open notepad"      "open vs code"
     "search latest AI news"                   "google python tips"
     "write a python function to reverse a string"
     "give me three ideas for a science project"
  Type instead of speaking any time. Say or type 'exit' to quit.
==================================================================
"""


class VoiceSession:
    """Runs the press-Enter-to-talk conversation loop."""

    def __init__(self) -> None:
        self.speaker = Speaker()
        self.listener = Listener()
        self.router = CommandRouter()

    def _get_command(self) -> str:
        """Block until the user is 'back on the terminal', then capture input."""
        try:
            typed = input("\n\033[1mPress ENTER to talk\033[0m "
                          "(or type a command, then Enter): ").strip()
        except EOFError:
            return "exit"
        if typed:
            return typed.lower()          # user typed a command instead
        return self.listener.listen()      # empty line -> voice mode

    def run(self) -> None:
        print(BANNER)
        if not self.listener.available:
            print("[!] Microphone stack not found - running in typed-input mode.")
            print("    Install with: pip install SpeechRecognition pyaudio\n")
        self.speaker.say("Voice assistant ready. Press enter whenever you want to talk to me.")

        while True:
            try:
                command = self._get_command()
                if not command:
                    continue
                reply = self.router.route(command)
                # Show the full answer (with any code) on screen...
                if reply.text != reply.speech:
                    print(reply.text)
                # ...and speak the concise version.
                self.speaker.say(reply.speech)
                if reply.should_exit:
                    break
            except KeyboardInterrupt:
                print("\nInterrupted. Goodbye!")
                break
            except Exception as exc:
                print(f"[error] {exc}")
                continue
