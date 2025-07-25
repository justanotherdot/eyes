import argparse
import sys
import time

from .reminders import create_reminder


def main():
    """Main function with command line argument support"""
    
    parser = argparse.ArgumentParser(
        description="Eyes - Configurable eye break reminder following the 20-20-20 rule"
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=20,
        help="Reminder interval in minutes (default: 20)",
    )
    parser.add_argument(
        "-s",
        "--snooze",
        type=int,
        default=5,
        help="Snooze duration in minutes (default: 5)",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Use simple notifications (no action buttons)",
    )
    parser.add_argument(
        "--test", action="store_true", help="Test mode - show notification immediately"
    )
    parser.add_argument("--version", action="version", version="eyes 1.0.0")

    args = parser.parse_args()

    if args.interval < 1:
        print("Error: Interval must be at least 1 minute")
        sys.exit(1)

    if args.snooze < 1:
        print("Error: Snooze duration must be at least 1 minute")
        sys.exit(1)

    # Create appropriate reminder for platform
    app = create_reminder(
        advanced=not args.simple,
        interval_minutes=args.interval,
        snooze_minutes=args.snooze
    )

    if args.test:
        print("Test mode - showing notification now...")
        app.show_reminder()
        time.sleep(2)
        return

    app.run()


def interactive_main():
    """Interactive setup for users who prefer guided configuration"""
    print("Eyes - Eye Break Reminder Setup")
    print("=" * 30)

    try:
        interval = input("Reminder interval in minutes (default 20): ").strip()
        interval = int(interval) if interval else 20

        if interval < 1:
            print("Interval must be at least 1 minute. Using default of 20.")
            interval = 20

    except (ValueError, KeyboardInterrupt):
        if "KeyboardInterrupt" in str(type(sys.exc_info()[0])):
            print("\nExiting...")
            return
        print("Invalid input. Using default of 20 minutes.")
        interval = 20

    try:
        snooze = input("Snooze duration in minutes (default 5): ").strip()
        snooze = int(snooze) if snooze else 5

        if snooze < 1:
            print("Snooze must be at least 1 minute. Using default of 5.")
            snooze = 5

    except (ValueError, KeyboardInterrupt):
        if "KeyboardInterrupt" in str(type(sys.exc_info()[0])):
            print("\nExiting...")
            return
        print("Invalid input. Using default of 5 minutes.")
        snooze = 5

    print("\nChoose reminder type:")
    print("1. Full-featured (with action buttons)")
    print("2. Simple (basic notifications)")

    try:
        choice = input("Enter choice (1 or 2): ").strip()
    except KeyboardInterrupt:
        print("\nExiting...")
        return

    if choice == "1":
        app = EyeBreakReminder(interval_minutes=interval, snooze_minutes=snooze)
    else:
        app = SimpleEyeBreakReminder(interval_minutes=interval)

    app.run()


def entry_point():
    """Main entry point"""
    main()

if __name__ == "__main__":
    entry_point()
