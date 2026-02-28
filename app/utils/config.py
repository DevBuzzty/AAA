import json
import os
from typing import Dict, Any, Optional

class Config:
    """
    Configuration manager for the AI agent.
    Handles settings like provider, model, API keys, etc.
    """
    CONFIG_PATH = os.path.expanduser("~/.config/ai-agent/config.json")

    def __init__(self):
        self.data: Dict[str, Any] = {
            "provider": "ollama",
            "model": "llama3",
            "gemini_api_key": "",
            "system_prompt": "Du bist ein hilfreicher KI-Assistent auf einem Ubuntu Headless Server.",
            "api_port": 8000,
            "api_host": "127.0.0.1",
            "repo_path": os.getcwd()
        }
        self.load()

    def load(self):
        if os.path.exists(self.CONFIG_PATH):
            try:
                with open(self.CONFIG_PATH, 'r') as f:
                    self.data.update(json.load(f))
            except Exception as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")

    def save(self):
        os.makedirs(os.path.dirname(self.CONFIG_PATH), exist_ok=True)
        try:
            with open(self.CONFIG_PATH, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
             print(f"Fehler beim Speichern der Konfiguration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self.save()
