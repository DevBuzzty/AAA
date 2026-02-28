import os
import subprocess
from typing import Dict, Any

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

# Registry for easy access
TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
    "execute_command": execute_command
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
    }
]
