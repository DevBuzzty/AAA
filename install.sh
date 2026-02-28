#!/bin/bash
set -e

echo "===================================================="
echo "   Arch AI Agent - Ubuntu Headless Server Installer"
echo "===================================================="

# 1. System-Abhängigkeiten installieren
sudo apt update && sudo apt install -y python3-pip python3-venv git curl

# 2. Ollama installieren (falls noch nicht vorhanden)
if ! command -v ollama >/dev/null 2>&1; then
    echo "Installiere Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    # Ollama Dienst starten (falls noch nicht geschehen)
    sudo systemctl enable --now ollama
    echo "Warte auf Ollama Dienst..."
    sleep 5
else
    echo "Ollama ist bereits installiert."
fi

# 3. Projekt-Verzeichnis vorbereiten (Pfad anpassen)
# In einem realen One-Liner wird das Repo hier geklont.
# Hier gehen wir davon aus, dass wir bereits im Zielverzeichnis sind oder das Repo klonen:
# git clone <repo_url> /opt/ai-agent
INSTALL_DIR="/opt/arch"
REPO_URL="https://github.com/DevBuzzty/AAA.git"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "Klone Repository in $INSTALL_DIR..."
    sudo git clone "$REPO_URL" "$INSTALL_DIR"
    sudo chown -R $(whoami):$(whoami) "$INSTALL_DIR"
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
sed "s|User=ubuntu|User=$(whoami)|g" scripts/arch.service.template | \
sed "s|Group=ubuntu|Group=$(id -gn)|g" | \
sed "s|/opt/arch|$INSTALL_DIR|g" > arch.service

sudo mv arch.service /etc/systemd/system/arch.service
sudo systemctl daemon-reload
sudo systemctl enable arch.service
sudo systemctl start arch.service

# 7. CLI Command link
echo "Erstelle 'arch' Befehl..."
echo "#!/bin/bash
$INSTALL_DIR/venv/bin/python $INSTALL_DIR/app/cli.py \"\$@\"" | sudo tee /usr/local/bin/arch > /dev/null
sudo chmod +x /usr/local/bin/arch

echo "===================================================="
echo "Installation abgeschlossen!"
echo "Du kannst Arch mit diesem Befehl nutzen:"
echo "arch help"
echo "Oder den Chat direkt starten:"
echo "arch chat"
echo "Viel Spaß mit deinem KI-Agenten Arch!"
echo "===================================================="
