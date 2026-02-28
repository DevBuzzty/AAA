from typing import List, Dict, Generator
import google.generativeai as genai
from .provider import LLMProvider

class GeminiProvider(LLMProvider):
    """
    Implementation of LLMProvider for Google Gemini API.
    Requires the 'google-generativeai' Python package.
    """
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Converts generic message formats into Gemini's format.
        Gemini uses 'user' and 'model' as roles.
        Note: The very first message can be a system prompt handled separately.
        """
        gemini_messages = []
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == "system":
                 # In a more advanced version, we'd initialize the model with a system_instruction.
                 # For simplicity, we just append it as a user message or ignore it if not handled by standard GenAI chat.
                 continue

            gemini_role = "user" if role == "user" else "model"
            gemini_messages.append({"role": gemini_role, "parts": [content]})
        return gemini_messages

    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            # For simplicity, using the direct generate_content approach
            # instead of stateful chat (which LLMManager handles manually).
            gemini_msgs = self._convert_messages(messages)
            response = self.model.generate_content(gemini_msgs)
            return response.text
        except Exception as e:
            return f"Error in Gemini generation: {str(e)}"

    def stream_response(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        try:
             gemini_msgs = self._convert_messages(messages)
             response = self.model.generate_content(gemini_msgs, stream=True)
             for chunk in response:
                 yield chunk.text
        except Exception as e:
             yield f"Error in Gemini stream: {str(e)}"

    def get_available_models(self) -> List[str]:
         # For simplicity, returning common models. Fetching from API requires more calls.
         return ["gemini-1.5-flash", "gemini-1.5-pro"]
