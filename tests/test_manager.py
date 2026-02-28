import unittest
from unittest.mock import MagicMock
from app.core.manager import Agent
from app.core.memory import Memory
from app.core.provider import LLMProvider

class TestLLMManager(unittest.TestCase):
    def test_ask_adds_to_history(self):
        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.generate_response.return_value = "Hallo!"

        memory = Memory()
        manager = Agent(mock_provider, memory)
        response = manager.ask("Hi", "System")

        self.assertEqual(response, "Hallo!")
        # Agent.ask adds 1 to history (user input). Assistant response is added by ask().
        self.assertEqual(len(manager.history), 2)
        self.assertEqual(manager.history[0]["role"], "user")
        self.assertEqual(manager.history[1]["role"], "assistant")

    def test_clear_history(self):
        mock_provider = MagicMock(spec=LLMProvider)
        memory = Memory()
        manager = Agent(mock_provider, memory)
        manager.history = [{"role": "user", "content": "Hi"}]
        manager.clear_history()
        self.assertEqual(len(manager.history), 0)

if __name__ == "__main__":
    unittest.main()
