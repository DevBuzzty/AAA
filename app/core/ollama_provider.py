from typing import List, Dict, Any, Generator
import ollama
from .provider import LLMProvider

class OllamaProvider(LLMProvider):
    """
    Implementation of LLMProvider for local Ollama instances.
    Requires the 'ollama' Python package.
    """
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name

    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            # Set keep_alive to 5m to avoid constant reloading (saves CPU on repeated requests)
            options = kwargs.pop("options", {})
            response = ollama.chat(model=self.model_name, messages=messages, options=options, keep_alive="5m", **kwargs)
            return response['message']['content']
        except Exception as e:
            return f"Error in Ollama generation: {str(e)}"

    def stream_response(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        try:
            options = kwargs.pop("options", {})
            stream = ollama.chat(model=self.model_name, messages=messages, stream=True, options=options, keep_alive="5m", **kwargs)
            for chunk in stream:
                yield chunk['message']['content']
        except Exception as e:
            yield f"Error in Ollama stream: {str(e)}"

    def get_available_models(self) -> List[str]:
        try:
            models_list = ollama.list()
            return [model['name'] for model in models_list['models']]
        except Exception as e:
            print(f"Error fetching Ollama models: {e}")
            return [self.model_name]
