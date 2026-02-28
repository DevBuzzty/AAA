import questionary
import os
import sys
import subprocess
from app.utils.config import Config

def run_onboarding():
    """
    Interactive onboarding script for setting up the AI agent.
    Collects API keys, selects model and provider, etc.
    """
    config = Config()

    print("Willkommen zum AI Agent Onboarding!")
    print("-----------------------------------")

    # 1. LLM Provider Auswahl
    provider = questionary.select(
        "Wähle deinen primären LLM Provider:",
        choices=["ollama", "gemini"]
    ).ask()
    config.set("provider", provider)

    # 2. Modell Auswahl
    if provider == "ollama":
        model_name = questionary.text(
            "Welches Ollama-Modell soll standardmäßig verwendet werden (Empfehlung: llama3:8b-instruct-q4_K_M für Performance)?",
            default="llama3"
        ).ask()
        config.set("model", model_name)

        # Automatisch das Modell pullen via Subprocess (robuster gegen Library-Issues)
        print(f"Prüfe/Pulle Ollama-Modell: {model_name}...")
        try:
            subprocess.run(["ollama", "pull", model_name], check=True)
            print(f"Modell {model_name} ist bereit.")
        except Exception as e:
            print(f"Warnung: Konnte Modell {model_name} nicht automatisch pullen. Bitte manuell 'ollama pull {model_name}' ausführen. Fehler: {e}")

    else:
        api_key = questionary.password("Gib deinen Google Gemini API Key ein:").ask()
        config.set("gemini_api_key", api_key)
        model_name = questionary.select(
            "Wähle ein Gemini-Modell:",
            choices=["gemini-1.5-flash", "gemini-1.5-pro"]
        ).ask()
        config.set("model", model_name)

    # 3. Brave Search API
    brave_key = questionary.password("Gib deinen Brave Search API Key ein (optional):").ask()
    if brave_key:
        config.set("brave_api_key", brave_key)

    # 4. Pfade
    repo_path = questionary.text(
        "Pfad zum Repository (für Updates):",
        default=os.getcwd()
    ).ask()
    config.set("repo_path", repo_path)

    # 4. System Prompt
    system_prompt = questionary.text(
        "Gib einen Standard-System-Prompt für den Agenten ein:",
        default="Du bist ein hilfreicher KI-Assistent auf einem Ubuntu Headless Server."
    ).ask()
    config.set("system_prompt", system_prompt)

    config.save()
    print("-----------------------------------")
    print("Onboarding abgeschlossen! Die Einstellungen wurden gespeichert.")

if __name__ == "__main__":
    run_onboarding()
