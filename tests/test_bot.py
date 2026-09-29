"""
Unit tests for the voice assistant's pure logic (no mic, no network, no AWS).

Run:
    venv\\Scripts\\python.exe -m unittest discover -s tests -v
"""

import unittest
from unittest import mock

from bot.tts import clean_for_speech
from bot.websearch import format_context, format_sources
from bot.router import CommandRouter, Reply, EXIT_WORDS, _spoken_summary


class FakeBrain:
    """A stand-in for the Bedrock brain so tests never hit the network."""

    def __init__(self, canned="a plain answer with no code"):
        self.canned = canned
        self.calls = []

    def answer(self, question, ground_with_search=False):
        self.calls.append(question)
        return self.canned


class TestSpeechCleaning(unittest.TestCase):
    def test_strips_code_blocks(self):
        text = "Here is code:\n```python\nprint('hi')\n```\nDone."
        self.assertNotIn("print", clean_for_speech(text))

    def test_strips_markdown_and_links(self):
        self.assertEqual(clean_for_speech("**bold** and [Google](http://g.co)"),
                         "bold and Google")


class TestSearchFormatting(unittest.TestCase):
    def setUp(self):
        self.hits = [{"title": "T1", "body": "B1", "href": "http://a"},
                     {"title": "T2", "body": "B2", "href": "http://b"}]

    def test_context_is_numbered(self):
        self.assertTrue(format_context(self.hits).startswith("1. T1"))

    def test_sources_and_empty(self):
        self.assertIn("http://a", format_sources(self.hits))
        self.assertEqual(format_context([]), "")


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = CommandRouter(brain=FakeBrain())

    def test_empty_command(self):
        self.assertIn("didn't catch", self.router.route("").text)

    def test_exit_intent(self):
        for word in ("exit", "quit", "goodbye"):
            self.assertTrue(self.router.route(word).should_exit)

    def test_general_question_uses_brain(self):
        reply = self.router.route("how do i reverse a list in python")
        self.assertEqual(reply.text, "a plain answer with no code")
        self.assertEqual(self.router.brain.calls[-1],
                         "how do i reverse a list in python")

    def test_search_intent_opens_google(self):
        # Patch the browser launch and the network call so nothing real happens.
        with mock.patch("bot.apps.google_search", return_value="") as g, \
             mock.patch("bot.router.web_search", return_value=[]):
            reply = self.router.route("search oriental institute of science")
            g.assert_called_once_with("oriental institute of science")
            self.assertIsInstance(reply, Reply)

    def test_google_keyword_searches_not_opens_homepage(self):
        with mock.patch("bot.apps.google_search", return_value="") as g, \
             mock.patch("bot.router.web_search", return_value=[]):
            self.router.route("google python tips")
            g.assert_called_once_with("python tips")

    def test_open_google_opens_site(self):
        with mock.patch("bot.apps.webbrowser.open") as wb:
            reply = self.router.route("open google")
            wb.assert_called_once()
            self.assertIn("Google", reply.text)

    def test_spoken_summary_hides_code(self):
        spoken = _spoken_summary("Sure.\n```py\nx=1\n```")
        self.assertIn("terminal", spoken)
        self.assertNotIn("x=1", spoken)


if __name__ == "__main__":
    unittest.main()
