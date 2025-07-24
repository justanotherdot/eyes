# Eyes

A configurable eye break reminder following the 20-20-20 rule.

## Quick install (binary)

Download the latest binary from releases and run:

```bash
# macOS/Linux
./eyes

# Windows
eyes.exe
```

## Build from source

```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and build
uv sync --dev
./bin/build

# Run the binary
./dist/eyes --help
```

## Install as startup service

### macOS
```bash
# After building, install as Launch Agent (auto-starts on login)
./bin/install-macos

# To uninstall
launchctl unload ~/Library/LaunchAgents/com.eyes.plist
rm ~/Library/LaunchAgents/com.eyes.plist
```

### Windows
```powershell
# After building, install to startup folder (auto-starts on login)
./bin/install-windows.ps1

# Custom interval
./bin/install-windows.ps1 -Interval 30

# To uninstall
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\eyes-startup.bat"
```

## Usage

```bash
eyes                    # Interactive setup
eyes -i 20              # Every 20 minutes  
eyes -i 25 -s 5         # Pomodoro (25 min work, 5 min break)
eyes --simple           # Simple notifications
eyes --test             # Test notification
```

## Examples

```bash
# Pomodoro technique (25 min work, 5 min break)
eyes -i 25 -s 5

# Hourly reminders  
eyes -i 60

# Frequent reminders for intensive work
eyes -i 10 -s 2

# Simple notifications every 45 minutes
eyes --simple -i 45
```