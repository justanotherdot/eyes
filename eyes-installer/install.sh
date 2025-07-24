#!/bin/sh -eu

# Eyes - Eye Break Reminder Installer

INSTALL_DIR="$HOME/.local/share/eyes"
PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$PLIST_DIR/com.eyes.plist"

echo "Installing Eyes Eye Break Reminder..."

# Create install directory
mkdir -p "$INSTALL_DIR"

# Copy files
cp eyes.pex "$INSTALL_DIR/"
cp eyes-control "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/eyes-control"

# Create LaunchAgents directory if needed
mkdir -p "$PLIST_DIR"

# Install plist with correct path
sed "s|EYES_PATH_PLACEHOLDER|$INSTALL_DIR|g" com.eyes.plist > "$PLIST_PATH"

# Load launch agent
launchctl load "$PLIST_PATH"

echo "✅ Eyes installed successfully!"
echo ""
echo "Eyes will now run in the background and remind you every 20 minutes."
echo ""
echo "Commands:"
echo "  $INSTALL_DIR/eyes-control show   - Show immediate reminder"
echo "  $INSTALL_DIR/eyes-control stop   - Stop the service"
echo "  $INSTALL_DIR/eyes-control status - Check if running"
echo ""
echo "To uninstall, run: ./uninstall.sh"
