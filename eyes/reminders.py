import platform
import sys


def create_reminder(advanced=False, interval_minutes=20, snooze_minutes=5):
    """Create platform-appropriate reminder instance"""
    system = platform.system()
    
    if system == "Darwin":
        from .platforms.macos.reminder import create_reminder as create_macos_reminder
        return create_macos_reminder(advanced, interval_minutes, snooze_minutes)
    elif system == "Windows":
        from .platforms.windows.reminder import create_reminder as create_windows_reminder
        return create_windows_reminder(advanced, interval_minutes, snooze_minutes)
    else:
        print(f"Unsupported platform: {system}")
        print("This app supports macOS and Windows.")
        sys.exit(1)