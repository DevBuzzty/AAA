#!/bin/bash
set -e

echo "===================================================="
echo "   AI Agent - Ubuntu Headless Server Installer"
echo "===================================================="

# 1. System-Abhängigkeiten installieren
sudo apt update && sudo apt install -y python3-pip python3-venv git curl

# 2. Ollama installieren (falls noch nicht vorhanden)
if ! command -v ollama >/dev/null 2>&1; then
    echo "Installiere Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    # Ollama Dienst starten (falls noch nicht geschehen)
    sudo systemctl enable --now ollama
else
    echo "Ollama ist bereits installiert."
fi

# 3. Projekt-Verzeichnis vorbereiten (Pfad anpassen)
# In einem realen One-Liner wird das Repo hier geklont.
# Hier gehen wir davon aus, dass wir bereits im Zielverzeichnis sind oder das Repo klonen:
# git clone <repo_url> /opt/ai-agent
INSTALL_DIR="/opt/ai-agent"
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Klone Repository in $INSTALL_DIR..."
    # Placeholder URL:
    # git clone https://github.com/REPLACE_ME/ai-agent.git "$INSTALL_DIR"
    sudo mkdir -p "$INSTALL_DIR"
    sudo chown $(whoami):$(whoami) "$INSTALL_DIR"
    # Aktuellen Inhalt kopieren (da wir in der Sandbox sind)
    cp -r . "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 4. Python Virtual Environment & Requirements
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install ollama google-generativeai fastapi uvicorn requests rich questionary pydantic

# 5. Onboarding ausführen
echo "Starte Onboarding..."
python3 -m scripts.onboarding

# 6. Systemd-Dienst einrichten
echo "Konfiguriere systemd-Service..."
# Template anpassen an aktuellen User und Pfad
sed "s|User=ubuntu|User=$(whoami)|g" scripts/ai-agent.service.template | \
sed "s|Group=ubuntu|Group=$(id -gn)|g" | \
sed "s|/opt/ai-agent|$INSTALL_DIR|g" > ai-agent.service

sudo mv ai-agent.service /etc/systemd/system/ai-agent.service
sudo systemctl daemon-reload
sudo systemctl enable ai-agent.service
sudo systemctl start ai-agent.service

echo "===================================================="
echo "Installation abgeschlossen!"
echo "Du kannst den Chatbot mit diesem Befehl starten:"
echo "$INSTALL_DIR/venv/bin/python -m app.ui.client"
echo "Viel Spaß mit deinem KI-Agenten!"
echo "===================================================="
