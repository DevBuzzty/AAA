import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Memory:
    """
    Manages the long-term memory and self-reflection of the agent.
    Stores facts, interactions, and insights about its own architecture.
    """
    MEMORY_PATH = os.path.expanduser("~/.config/ai-agent/memory.json")

    def __init__(self):
        self.data: Dict[str, Any] = {
            "facts": [],
            "reflections": [],
            "learned_patterns": {},
            "last_interaction": None
        }
        self.load()

    def load(self):
        if os.path.exists(self.MEMORY_PATH):
            try:
                with open(self.MEMORY_PATH, 'r') as f:
                    self.data.update(json.load(f))
            except Exception as e:
                print(f"Fehler beim Laden des Gedächtnisses: {e}")

    def save(self):
        os.makedirs(os.path.dirname(self.MEMORY_PATH), exist_ok=True)
        try:
            with open(self.MEMORY_PATH, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
             print(f"Fehler beim Speichern des Gedächtnisses: {e}")

    def add_fact(self, fact: str):
        self.data["facts"].append({
            "timestamp": datetime.now().isoformat(),
            "content": fact
        })
        self.save()

    def add_reflection(self, insight: str):
        self.data["reflections"].append({
            "timestamp": datetime.now().isoformat(),
            "content": insight
        })
        self.save()

    def get_context_string(self) -> str:
        """Returns a summarized string of memory for LLM context."""
        summary = "Bisheriges Wissen über mich und meine Umgebung:\n"
        if not self.data["facts"] and not self.data["reflections"]:
            return summary + "- Noch keine Erinnerungen vorhanden."

        for fact in self.data["facts"][-10:]: # Letzte 10 Fakten
            summary += f"- Fakt: {fact['content']}\n"
        for reflection in self.data["reflections"][-5:]: # Letzte 5 Reflexionen
            summary += f"- Erkenntnis: {reflection['content']}\n"
        return summary
