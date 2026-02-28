import unittest
from unittest.mock import MagicMock
from app.core.manager import Agent
from app.core.memory import Memory
from app.core.provider import LLMProvider

class TestAgent(unittest.TestCase):
    def test_agent_tool_use_logic(self):
        mock_provider = MagicMock(spec=LLMProvider)
        # Mocking a tool call JSON response
        mock_provider.stream_response.side_effect = [
            iter(['{"tool": "read_file", "args": {"filepath": "test.txt"}}']),
            iter(['Inhalt von test.txt ist: Hallo'])
        ]

        memory = Memory()
        agent = Agent(mock_provider, memory)

        # Mocking the tool itself to avoid disk access
        import app.core.tools
        app.core.tools.TOOLS["read_file"] = MagicMock(return_value="Inhalt von test.txt")

        response = agent.ask("Lies test.txt", "System")

        # Note: final response in streaming mode might contain [System: ...] marker if we use stream() directly
        # but ask() joins it. Let's adjust expectations.
        self.assertIn("Inhalt von test.txt ist: Hallo", response)
        app.core.tools.TOOLS["read_file"].assert_called_with(filepath="test.txt")

if __name__ == "__main__":
    unittest.main()
