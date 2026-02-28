from abc import ABC, abstractmethod
from typing import Generator, List, Dict, Any

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers (Strategy Pattern).
    Ensures that adding new providers like Gemini requires minimal refactoring.
    """

    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generates a full response from the LLM.
        """
        pass

    @abstractmethod
    def stream_response(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        """
        Streams the response from the LLM.
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Returns a list of available models for this provider.
        """
        pass
