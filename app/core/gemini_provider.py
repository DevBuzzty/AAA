from typing import List, Dict, Generator
import google.generativeai as genai
from .provider import LLMProvider

class GeminiProvider(LLMProvider):
    """
    Implementation of LLMProvider for Google Gemini API.
    """
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def _convert_messages(self, messages: List[Dict[str, str]]):
        """
        Converts generic message formats into Gemini's format.
        Handles system messages by prepending them to the user context
        or using Gemini's system_instruction if available.
        """
        gemini_msgs = []
        system_content = ""

        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == "system":
                system_content += content + "\n"
                continue

            gemini_role = "user" if role == "user" else "model"
            # If we had a system prompt, prepend it to the first user message
            if system_content and gemini_role == "user" and not gemini_msgs:
                content = f"SYSTEM INSTRUCTIONS:\n{system_content}\n\nUSER MESSAGE:\n{content}"
                system_content = "" # Reset so we don't prepend again

            gemini_msgs.append({"role": gemini_role, "parts": [content]})
        return gemini_msgs

    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
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
         return ["gemini-1.5-flash", "gemini-1.5-pro"]
