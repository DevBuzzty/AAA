import argparse
import sys
import os
import subprocess
import requests

# Set PYTHONPATH to project root to allow relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.config import Config

def main():
    parser = argparse.ArgumentParser(prog="arch", description="Arch AI Agent CLI")
    subparsers = parser.add_subparsers(dest="command", help="Verfügbare Befehle")

    # arch chat
    subparsers.add_parser("chat", help="Startet den interaktiven Chatbot")

    # arch onboarding
    subparsers.add_parser("onboarding", help="Startet das Onboarding / die Konfiguration")

    # arch update
    subparsers.add_parser("update", help="Zieht den neuesten Code vom Repository und startet den Dienst neu")

    # arch status
    subparsers.add_parser("status", help="Zeigt den Status des Brain-Dienstes an")

    # arch restart
    subparsers.add_parser("restart", help="Startet den Brain-Dienst neu")

    # arch pull <model>
    pull_parser = subparsers.add_parser("pull", help="Lad ein Ollama Modell herunter")
    pull_parser.add_argument("model", help="Name des Modells (z.B. llama3)")

    args = parser.parse_args()

    config = Config()
    brain_url = f"http://{config.get('api_host', '127.0.0.1')}:{config.get('api_port', 8000)}"

    if args.command == "chat":
        from app.ui.client import chat_loop
        chat_loop()

    elif args.command == "onboarding":
        from scripts.onboarding import run_onboarding
        run_onboarding()

    elif args.command == "update":
        print("Aktualisiere Arch...")
        try:
            requests.post(f"{brain_url}/update")
            print("Update-Befehl gesendet. Dienst startet neu.")
        except:
            # If brain is offline, try manual git pull
            repo_path = config.get("repo_path", os.getcwd())
            subprocess.run(["git", "-C", repo_path, "pull"])
            subprocess.run(["sudo", "systemctl", "restart", "arch.service"])
            print("Manueller Update durchgeführt.")

    elif args.command == "status":
        try:
            r = requests.get(f"{brain_url}/status")
            print(f"Brain Status: {r.json()}")
        except:
            print("Brain ist OFFLINE.")
        subprocess.run(["sudo", "systemctl", "status", "arch.service"])

    elif args.command == "restart":
        subprocess.run(["sudo", "systemctl", "restart", "arch.service"])
        print("Dienst neu gestartet.")

    elif args.command == "pull":
        print(f"Pulle Modell {args.model} via Ollama...")
        subprocess.run(["ollama", "pull", args.model])

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
