# Eyes

A configurable eye break reminder following the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds.

## Features

- **Cross-platform**: macOS and Windows support
- **Background service**: Runs quietly without dock/taskbar presence  
- **Runtime control**: Signal-based IPC for immediate notifications and shutdown
- **Professional installers**: Native .pkg (macOS) and GUI installers
- **Flexible timing**: Configurable intervals and snooze duration

## Quick install

### macOS
Download and run the installer:
```bash
# GUI installer (recommended)
./bin/installers/create-pkg-installer  # Creates Eyes-1.0.0.pkg
# Double-click Eyes-1.0.0.pkg

# Command-line installer
./bin/installers/create-installer      # Creates eyes-installer/
cd eyes-installer && ./install
```

### Windows  
```bash
./bin/installers/create-installer      # Creates eyes-installer/
cd eyes-installer && ./install
```

## Development setup

```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies  
uv sync --dev

# Run directly
uv run eyes --test
```

## Platform services

### macOS Launch Agent
```bash
# Install background service (auto-starts on login)
./bin/macos/install-macos

# Control running service
./bin/macos/eyes-control show    # Immediate notification
./bin/macos/eyes-control stop    # Stop service
./bin/macos/eyes-control status  # Check status

# Uninstall
./bin/macos/uninstall-macos
```

### Windows startup
```powershell
./bin/windows/install-windows.ps1
```

## Usage

```bash
# Basic usage
uv run eyes                    # Default 20-minute intervals
uv run eyes -i 30              # Every 30 minutes  
uv run eyes -i 25 -s 5         # Advanced with snooze (25 min work, 5 min snooze)
uv run eyes --simple -i 45     # Simple notifications, no snooze
uv run eyes --test             # Test notification immediately
```

## Architecture

```
eyes/
├── core/           # Platform-agnostic reminder logic
│   └── reminder.py # BaseReminder, AdvancedReminder classes
├── platforms/      # Platform-specific implementations
│   ├── macos/      # macOS notifications, Launch Agent config
│   └── windows/    # Windows notifications, startup scripts
├── reminders.py    # Platform detection and reminder creation
└── cli.py          # Command-line interface

bin/
├── macos/          # macOS utilities (eyes-control, install/uninstall)  
├── windows/        # Windows utilities
└── installers/     # Cross-platform installer builders
```

## Examples

```bash
# Pomodoro technique (25 min work, 5 min snooze)
uv run eyes -i 25 -s 5

# Hourly reminders  
uv run eyes -i 60

# Frequent reminders for intensive work
uv run eyes -i 10 -s 2

# Simple notifications every 45 minutes (no advanced features)
uv run eyes --simple -i 45
```