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

    def ask(self, user_input: str, base_system_prompt: str) -> str:
        system_prompt = self._get_system_prompt(base_system_prompt)

        # We handle system prompt as the first message or a persistent context
        messages = [{"role": "system", "content": system_prompt}] + self.history + [{"role": "user", "content": user_input}]
        self.history.append({"role": "user", "content": user_input})

        # Simple loop for tool usage (1 step for now)
        response = self.provider.generate_response(messages)

        tool_call = self._extract_json(response)
        if tool_call and isinstance(tool_call, dict) and "tool" in tool_call:
            tool_name = tool_call["tool"]
            args = tool_call.get("args", {})

            if tool_name in TOOLS:
                try:
                    result = TOOLS[tool_name](**args)
                    # Tell the LLM about the tool result
                    tool_msg = f"Tool Ergebnis ({tool_name}): {result}"
                    self.memory.add_fact(f"Ich habe das Tool {tool_name} genutzt.")

                    # Get final response from LLM after tool use
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "system", "content": tool_msg})
                    final_response = self.provider.generate_response(messages)
                    self.history.append({"role": "assistant", "content": final_response})
                    return final_response
                except Exception as e:
                    # Tool execution failed
                    self.history.append({"role": "assistant", "content": response})
                    return f"Tool Fehler: {str(e)}"

        self.history.append({"role": "assistant", "content": response})
        return response

    def clear_history(self):
        self.history = []
