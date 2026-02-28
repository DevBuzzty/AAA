# Arch - Ubuntu Headless AI Agent

Arch ist ein modularer, erweiterbarer KI-Agent mit lokaler Ollama-Unterstützung und Google Gemini API-Anbindung. Er verfügt über ein Gedächtnis, Werkzeuge zur Systeminteraktion und die Fähigkeit zur Selbstprogrammierung.

## Features
- **Strategy Pattern:** Einfaches Umschalten zwischen Ollama und Gemini (weitere Provider leicht hinzufügbar).
- **Brain Service:** Ein Hintergrunddienst (FastAPI), der über `systemd` läuft und den Chatverlauf verwaltet.
- **TUI Client:** Ein schicker Terminal-User-Interface Client mit Markdown-Unterstützung.
- **Update-Mechanismus:** Direktes Updaten über das Terminal (`/update`).
- **Onboarding:** Einfaches Setup beim ersten Start.

## Schnelles Setup (One-Liner)

Um Arch auf einem frischen Ubuntu Headless Server zu installieren:

```bash
git clone https://github.com/DevBuzzty/AAA.git arch && cd arch && bash install.sh
```

## CLI Bedienung (arch)
Nach der Installation steht der Befehl `arch` systemweit zur Verfügung:

- `arch chat`: Startet das interaktive Terminal-Interface.
- `arch update`: Zieht den neuesten Code von GitHub und startet den Dienst neu.
- `arch onboarding`: Startet die Konfiguration neu (Modellwahl, API-Keys).
- `arch pull <model>`: Lädt ein spezifisches Modell für Ollama herunter.
- `arch status`: Zeigt den Status des Hintergrunddienstes.
- `arch restart`: Startet den Dienst manuell neu.

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
