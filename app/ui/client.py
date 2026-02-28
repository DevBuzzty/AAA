import requests
import rich
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from app.utils.config import Config
import sys
import os

console = Console()
config = Config()

BRAIN_URL = f"http://{config.get('api_host', '127.0.0.1')}:{config.get('api_port', 8000)}"

def send_to_brain(message: str) -> str:
    try:
        response = requests.post(f"{BRAIN_URL}/chat", json={"message": message})
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Fehler bei der Verbindung zum Brain: {str(e)}"

def update_brain():
    try:
        response = requests.post(f"{BRAIN_URL}/update")
        response.raise_for_status()
        console.print("[bold yellow]Brain wird aktualisiert und neu gestartet...[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Fehler beim Update: {str(e)}[/bold red]")

def chat_loop():
    console.print(Panel("[bold cyan]KI Agent Terminal Client[/bold cyan]\nVerwende '/exit' zum Beenden, '/update' für Git Pull & Restart, '/clear' zum Verlauf löschen.", border_style="blue"))

    while True:
        user_input = Prompt.ask("[bold green]Du[/bold green]")

        if user_input.lower() == "/exit":
            console.print("[yellow]Verlasse Terminal Client...[/yellow]")
            break

        if user_input.lower() == "/update":
            if Prompt.ask("Update wirklich durchführen?", choices=["y", "n"]) == "y":
                 update_brain()
                 # Optional: Wait and restart client too?
                 break
            continue

        if user_input.lower() == "/clear":
             requests.post(f"{BRAIN_URL}/clear")
             console.print("[yellow]Chat-Verlauf gelöscht.[/yellow]")
             continue

        with console.status("[bold blue]Agent denkt nach...[/bold blue]"):
            response = send_to_brain(user_input)

        # Check if response looks like a tool call (JSON)
        if response.startswith("{") and response.endswith("}"):
            try:
                import json
                tool_data = json.loads(response)
                if "tool" in tool_data:
                    console.print(f"[bold yellow]Tool Aufruf:[/bold yellow] {tool_data['tool']}({tool_data.get('args', {})})")
            except:
                pass

        console.print(Panel(Markdown(response), title="[bold magenta]KI Agent[/bold magenta]", border_style="magenta"))

if __name__ == "__main__":
    chat_loop()
