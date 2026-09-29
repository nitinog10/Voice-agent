"""
bot.llm  -  The reasoning brain (AWS Bedrock, Amazon Nova)
=========================================================
Answers free-form questions, helps write and explain code, and brainstorms
ideas by calling the AWS Bedrock **Converse** API. Optionally grounds answers
with live web-search results so current facts are accurate.

The Bedrock client is created lazily and cached, so we only pay the connection
cost once and only if the assistant actually needs to think.
"""

from __future__ import annotations

from .config import config
from . import websearch

try:
    import boto3
except ImportError:
    boto3 = None

SYSTEM_PROMPT = (
    "You are a capable, friendly voice assistant. You can answer questions, "
    "explain and write code, and help brainstorm ideas. Speak naturally, as if "
    "talking to a person. Keep spoken explanations concise and clear. When you "
    "write code, put it inside fenced code blocks so it can be shown on screen. "
    "If web search results are provided, rely on them and prefer recent facts."
)


class Brain:
    """Wraps Bedrock Converse with optional web grounding."""

    def __init__(self) -> None:
        self._client = None

    def _bedrock(self):
        if self._client is not None:
            return self._client
        if boto3 is None or not config.has_bedrock_credentials():
            return None
        self._client = boto3.client(
            "bedrock-runtime",
            region_name=config.aws_region,
            aws_access_key_id=config.aws_access_key,
            aws_secret_access_key=config.aws_secret_key,
        )
        return self._client

    def answer(self, question: str, ground_with_search: bool = False) -> str:
        """Return a full text answer (may contain fenced code)."""
        client = self._bedrock()
        if client is None:
            return ("My AWS Bedrock brain isn't configured. Add your IAM keys to "
                    "the .env file and install boto3, then try again.")

        user_text = question
        if ground_with_search or (config.use_web_search and _looks_current(question)):
            hits = websearch.web_search(question)
            context = websearch.format_context(hits)
            if context:
                user_text = (f"Question: {question}\n\n"
                             f"Web search results:\n{context}\n\n"
                             f"Answer using these results.")

        try:
            resp = client.converse(
                modelId=config.model_id,
                messages=[{"role": "user", "content": [{"text": user_text}]}],
                system=[{"text": SYSTEM_PROMPT}],
                inferenceConfig={"maxTokens": 600, "temperature": 0.5},
            )
            return resp["output"]["message"]["content"][0]["text"].strip()
        except Exception as exc:
            return f"My Bedrock request failed: {exc}"


def _looks_current(text: str) -> bool:
    """Heuristic: does the question likely need fresh web facts?"""
    keywords = ("latest", "today", "news", "current", "now", "2024", "2025",
                "2026", "who is", "price", "weather", "score", "recent")
    return any(k in text.lower() for k in keywords)
