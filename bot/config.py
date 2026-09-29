"""
bot.config
==========
Central configuration for the voice assistant.

Every tunable value is read once from the `.env` file (via python-dotenv) and
exposed as attributes on a single `Config` object. Keeping configuration in one
place means no other module has to touch `os.environ`, which makes the codebase
easy to read, test, and maintain.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # dotenv is optional; env vars may already be set
    pass


def _flag(name: str, default: str = "false") -> bool:
    """Read a boolean-ish environment variable."""
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


@dataclass
class Config:
    """All runtime settings, loaded from the environment."""

    # --- AWS Bedrock (the "brain") ---
    aws_region: str = field(default_factory=lambda: os.getenv("AWS_REGION", "ap-south-1"))
    aws_access_key: str = field(default_factory=lambda: os.getenv("AWS_ACCESS_KEY_ID", ""))
    aws_secret_key: str = field(default_factory=lambda: os.getenv("AWS_SECRET_ACCESS_KEY", ""))
    model_id: str = field(default_factory=lambda: os.getenv("BEDROCK_MODEL_ID", "apac.amazon.nova-lite-v1:0"))

    # --- Speech ---
    speech_rate: int = field(default_factory=lambda: int(os.getenv("SPEECH_RATE", "175")))
    voice_gender: str = field(default_factory=lambda: os.getenv("VOICE_GENDER", "female").lower())
    listen_seconds: int = field(default_factory=lambda: int(os.getenv("LISTEN_SECONDS", "7")))
    phrase_limit: int = field(default_factory=lambda: int(os.getenv("PHRASE_LIMIT_SECONDS", "20")))
    pause_threshold: float = field(default_factory=lambda: float(os.getenv("PAUSE_THRESHOLD", "0.9")))

    # --- Behaviour ---
    use_web_search: bool = field(default_factory=lambda: _flag("USE_WEB_SEARCH", "true"))

    def has_bedrock_credentials(self) -> bool:
        return bool(self.aws_access_key and self.aws_secret_key)

    def masked_key(self) -> str:
        """A safe, non-secret preview of the access key for logs/UI."""
        k = self.aws_access_key
        return f"{k[:4]}…{k[-4:]}" if len(k) >= 8 else "(unset)"


# A single shared instance used across the app.
config = Config()
