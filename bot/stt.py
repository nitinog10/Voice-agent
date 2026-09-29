"""
bot.stt  -  Speech-to-Text (the assistant's ears)
=================================================
Captures one spoken command from the microphone and returns the transcribed
text using Google's free Web Speech recogniser (no API key, needs internet).

Listening behaviour (as required):
  * Waits up to `LISTEN_SECONDS` (default 7s) for the user to START speaking.
  * Keeps recording until the user PAUSES (`pause_threshold`), then transcribes.
  * `phrase_limit` caps a single utterance so it can never hang forever.

If the microphone stack (SpeechRecognition / PyAudio) is unavailable, the
recogniser degrades gracefully to typed keyboard input.
"""

from __future__ import annotations

from .config import config

try:
    import speech_recognition as sr
except ImportError:
    sr = None


class Listener:
    """Turns speech from the microphone into lowercased text."""

    def __init__(self) -> None:
        self.available = sr is not None
        if self.available:
            self._recognizer = sr.Recognizer()
            self._recognizer.pause_threshold = config.pause_threshold

    def listen(self) -> str:
        """Capture one utterance. Returns lowercased text, or '' on failure."""
        if not self.available:
            return input("[type your command] > ").strip().lower()

        try:
            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print(f"\033[96m[listening]\033[0m speak now "
                      f"(you have {config.listen_seconds}s to begin)…")
                audio = self._recognizer.listen(
                    source,
                    timeout=config.listen_seconds,
                    phrase_time_limit=config.phrase_limit,
                )
        except sr.WaitTimeoutError:
            print("[stt] I didn't hear anything.")
            return ""
        except Exception as exc:
            print(f"[stt] microphone error: {exc}")
            return ""

        return self._transcribe(audio)

    def _transcribe(self, audio) -> str:
        try:
            text = self._recognizer.recognize_google(audio)
            print(f"\033[93m[you]\033[0m {text}")
            return text.lower().strip()
        except sr.UnknownValueError:
            print("[stt] sorry, I couldn't understand that.")
            return ""
        except sr.RequestError as exc:
            print(f"[stt] speech service error: {exc}")
            return ""
