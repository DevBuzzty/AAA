import json
from typing import List, Dict, Optional, Any
from .provider import LLMProvider
from .memory import Memory
from .tools import TOOLS, TOOL_DEFINITIONS

class Agent:
    """
    Advanced Agent class that manages memory, tools, and self-evolution.
    """
    def __init__(self, provider: LLMProvider, memory: Memory):
        self.provider = provider
        self.memory = memory
        self.history: List[Dict[str, str]] = []

    def _get_system_prompt(self, base_prompt: str) -> str:
        memory_context = self.memory.get_context_string()
        tools_desc = json.dumps(TOOL_DEFINITIONS, indent=2)

        return f"{base_prompt}\n\n{memory_context}\n\n" \
               f"Du hast Zugriff auf folgende Tools. Um ein Tool zu nutzen, antworte AUSSCHLIEẞLICH mit einem JSON-Objekt im Format: " \
               f"{{\"tool\": \"name\", \"args\": {{\"arg1\": \"val1\"}}}}\n\n" \
               f"Tools:\n{tools_desc}\n\n" \
               f"Du kannst dich selbst umprogrammieren, indem du write_file auf deine eigenen Dateien anwendest."

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extracts JSON from a string, handling markdown code blocks."""
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(text)
        except:
            return None

    def stream(self, user_input: str, base_system_prompt: str):
        """
        Streaming version of ask() for better user experience.
        Optimized to handle long history (max 10 messages) to save RAM/CPU.
        """
        system_prompt = self._get_system_prompt(base_system_prompt)

        # Keep only the last 10 messages for context efficiency
        context_history = self.history[-10:]
        messages = [{"role": "system", "content": system_prompt}] + context_history + [{"role": "user", "content": user_input}]

        self.history.append({"role": "user", "content": user_input})

        full_response = ""
        # Check if the provider can stream
        for chunk in self.provider.stream_response(messages):
            full_response += chunk
            yield chunk

        # Check for tool call after streaming
        tool_call = self._extract_json(full_response)
        if tool_call and isinstance(tool_call, dict) and "tool" in tool_call:
            tool_name = tool_call["tool"]
            args = tool_call.get("args", {})

            if tool_name in TOOLS:
                try:
                    result = TOOLS[tool_name](**args)
                    tool_msg = f"\n\n[System: Tool Ergebnis ({tool_name}): {result}]\n\n"
                    yield tool_msg

                    self.memory.add_fact(f"Ich habe das Tool {tool_name} genutzt.")

                    messages.append({"role": "assistant", "content": full_response})
                    messages.append({"role": "system", "content": f"Tool Ergebnis ({tool_name}): {result}"})

                    final_response = ""
                    for chunk in self.provider.stream_response(messages):
                        final_response += chunk
                        yield chunk
                    self.history.append({"role": "assistant", "content": final_response})
                    return
                except Exception as e:
                    yield f"\nTool Fehler: {str(e)}"

        self.history.append({"role": "assistant", "content": full_response})

    def ask(self, user_input: str, base_system_prompt: str) -> str:
        # Keep original ask() for backward compatibility/simplicity
        gen = self.stream(user_input, base_system_prompt)
        return "".join(list(gen))

    def clear_history(self):
        self.history = []
