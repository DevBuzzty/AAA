import os
import subprocess
import requests
from typing import Dict, Any
from app.utils.config import Config

config = Config()

def read_file(filepath: str) -> str:
    """Reads a file from the disk."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(filepath: str, content: str) -> str:
    """Writes or updates a file on the disk."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully written to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def execute_command(command: str) -> str:
    """Executes a shell command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def search_internet(query: str) -> str:
    """Sucht im Internet via Brave Search API."""
    api_key = config.get("brave_api_key")
    if not api_key:
        return "Brave Search API Key nicht konfiguriert."

    headers = {"Accept": "application/json", "X-Subscription-Token": api_key}
    try:
        response = requests.get(f"https://api.search.brave.com/res/v1/web/search?q={query}", headers=headers)
        response.raise_for_status()
        results = response.json().get("web", {}).get("results", [])

        summary = ""
        for res in results[:3]:
            summary += f"Titel: {res['title']}\nURL: {res['url']}\nInhalt: {res['description']}\n\n"
        return summary or "Keine Ergebnisse gefunden."
    except Exception as e:
        return f"Fehler bei der Suche: {str(e)}"

# Registry for easy access
TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
    "execute_command": execute_command,
    "search_internet": search_internet
}

TOOL_DEFINITIONS = [
    {
        "name": "read_file",
        "description": "Liest den Inhalt einer Datei.",
        "parameters": ["filepath"]
    },
    {
        "name": "write_file",
        "description": "Schreibt Inhalt in eine Datei (Self-Programming!).",
        "parameters": ["filepath", "content"]
    },
    {
        "name": "execute_command",
        "description": "Führt einen Shell-Befehl auf dem Server aus.",
        "parameters": ["command"]
    },
    {
        "name": "search_internet",
        "description": "Sucht im Internet nach aktuellen Informationen.",
        "parameters": ["query"]
    }
]
