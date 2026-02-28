#!/bin/bash
# Standalone Update Script

# Configuration - should be configurable in the future
REPO_DIR="$(dirname "$(realpath "$0")")/.."
CONFIG_PATH="$HOME/.config/ai-agent/config.json"

echo "Checking for updates in $REPO_DIR..."

cd "$REPO_DIR"
git pull

# Check if we should restart the service
if command -v systemctl >/dev/null 2>&1; then
    echo "Restarting service..."
    sudo systemctl restart ai-agent.service
else
    echo "Systemd not found. Please restart the process manually."
fi

echo "Update complete."
