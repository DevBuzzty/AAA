from typing import List, Dict, Optional
from .provider import LLMProvider

class LLMManager:
    """
    Manages LLM providers and model selection.
    """
    def __init__(self, provider: LLMProvider):
        self._provider = provider
        self.history: List[Dict[str, str]] = []

    def set_provider(self, provider: LLMProvider):
        self._provider = provider

    def ask(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if system_prompt and not self.history:
            self.history.append({"role": "system", "content": system_prompt})

        self.history.append({"role": "user", "content": prompt})
        response = self._provider.generate_response(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response

    def stream(self, prompt: str, system_prompt: Optional[str] = None):
        if system_prompt and not self.history:
             self.history.append({"role": "system", "content": system_prompt})

        self.history.append({"role": "user", "content": prompt})
        full_response = ""
        for chunk in self._provider.stream_response(self.history):
            full_response += chunk
            yield chunk
        self.history.append({"role": "assistant", "content": full_response})

    def clear_history(self):
        self.history = []
