# AI Agent - Ubuntu Headless Terminal Chatbot

Ein modularer, erweiterbarer KI-Agent mit lokaler Ollama-Unterstützung und Google Gemini API-Anbindung.

## Features
- **Strategy Pattern:** Einfaches Umschalten zwischen Ollama und Gemini (weitere Provider leicht hinzufügbar).
- **Brain Service:** Ein Hintergrunddienst (FastAPI), der über `systemd` läuft und den Chatverlauf verwaltet.
- **TUI Client:** Ein schicker Terminal-User-Interface Client mit Markdown-Unterstützung.
- **Update-Mechanismus:** Direktes Updaten über das Terminal (`/update`).
- **Onboarding:** Einfaches Setup beim ersten Start.

## Schnelles Setup (One-Liner)

Um den Agenten auf einem frischen Ubuntu Headless Server zu installieren:

```bash
# Ersetze <REPO_URL> durch den tatsächlichen GitHub-Link
git clone <REPO_URL> ai-agent && cd ai-agent && bash install.sh
```

## Manuelle Installation

1. **System-Abhängigkeiten:**
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-venv git curl
   ```

2. **Ollama (optional für lokalen Betrieb):**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

3. **Abhängigkeiten:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Service starten:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable ai-agent.service
   sudo systemctl start ai-agent.service
   ```

## Bedienung

Starte den Terminal-Client:
```bash
python3 -m app.ui.client
```

Befehle im Chat:
- `/update`: Zieht den neuesten Code von GitHub und startet den Dienst neu.
- `/clear`: Löscht den aktuellen Chat-Verlauf.
- `/exit`: Beendet den Client.

## Konfiguration
Die Konfiguration wird in `~/.config/ai-agent/config.json` gespeichert.
Du kannst das Onboarding jederzeit erneut starten:
```bash
python3 -m scripts.onboarding
```
