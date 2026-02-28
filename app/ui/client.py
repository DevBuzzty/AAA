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

def send_to_brain_stream(message: str):
    """
    Consumes the streaming response from the Brain.
    """
    try:
        with requests.post(f"{BRAIN_URL}/chat", json={"message": message}, stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    yield chunk
    except Exception as e:
        yield f"Fehler bei der Verbindung zum Brain: {str(e)}"

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

        console.print(Panel("", title="[bold magenta]Arch[/bold magenta]", border_style="magenta"), end="")

        full_response = ""
        # Create a live display for streaming
        from rich.live import Live
        with Live(console=console, refresh_per_second=10) as live:
            for chunk in send_to_brain_stream(user_input):
                full_response += chunk
                live.update(Panel(Markdown(full_response), title="[bold magenta]Arch[/bold magenta]", border_style="magenta"))

if __name__ == "__main__":
    chat_loop()
