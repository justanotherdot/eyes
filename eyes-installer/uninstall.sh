#!/bin/sh -eu

# Eyes - Eye Break Reminder Uninstaller

INSTALL_DIR="$HOME/.local/share/eyes"
PLIST_PATH="$HOME/Library/LaunchAgents/com.eyes.plist"

echo "Uninstalling Eyes Eye Break Reminder..."

# Stop and remove launch agent
if [ -f "$PLIST_PATH" ]; then
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    rm "$PLIST_PATH"
fi

# Remove installed files
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
fi

echo "✅ Eyes uninstalled successfully!"
