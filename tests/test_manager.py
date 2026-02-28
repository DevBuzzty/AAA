import unittest
from unittest.mock import MagicMock
from app.core.manager import LLMManager
from app.core.provider import LLMProvider

class TestLLMManager(unittest.TestCase):
    def test_ask_adds_to_history(self):
        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.generate_response.return_value = "Hallo!"

        manager = LLMManager(mock_provider)
        response = manager.ask("Hi")

        self.assertEqual(response, "Hallo!")
        self.assertEqual(len(manager.history), 2)
        self.assertEqual(manager.history[0]["role"], "user")
        self.assertEqual(manager.history[1]["role"], "assistant")

    def test_clear_history(self):
        mock_provider = MagicMock(spec=LLMProvider)
        manager = LLMManager(mock_provider)
        manager.history = [{"role": "user", "content": "Hi"}]
        manager.clear_history()
        self.assertEqual(len(manager.history), 0)

if __name__ == "__main__":
    unittest.main()
