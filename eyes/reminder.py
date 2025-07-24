import time
import threading
import platform
import sys
import signal


class EyeBreakReminder:
    def __init__(self, interval_minutes=20, snooze_minutes=5):
        self.is_reminder_active = False
        self.should_run = True
        self.system = platform.system()
        self.interval_minutes = interval_minutes
        self.snooze_minutes = snooze_minutes

        print(f"Reminder interval: {interval_minutes} minutes")
        print(f"Snooze duration: {snooze_minutes} minutes")
        
        # Set up signal handlers
        signal.signal(signal.SIGUSR1, self._signal_show_reminder)
        signal.signal(signal.SIGTERM, self._signal_shutdown)

        if self.system == "Windows":
            self.setup_windows_notifications()
        elif self.system == "Darwin":
            self.setup_macos_notifications()
        else:
            print("Unsupported platform. This app works on Windows 11 and macOS.")
            sys.exit(1)

    def setup_windows_notifications(self):
        try:
            import plyer

            self.notification_method = "plyer"
        except ImportError:
            try:
                import win10toast

                self.toaster = win10toast.ToastNotifier()
                self.notification_method = "win10toast"
            except ImportError:
                try:
                    from winotify import Notification

                    self.notification_method = "winotify"
                except ImportError:
                    print("Please install notification support:")
                    print("pip install winotify")
                    print("or: pip install plyer")
                    sys.exit(1)

    def setup_macos_notifications(self):
        try:
            import pync

            self.notification_method = "pync"
        except ImportError:
            try:
                import plyer

                self.notification_method = "plyer"
            except ImportError:
                print("Please install notification support:")
                print("pip install pync")
                print("or: pip install plyer")
                sys.exit(1)

    def show_notification(self, title, message, actions=None):
        if self.is_reminder_active:
            return

        self.is_reminder_active = True

        if self.system == "Windows":
            self._show_windows_notification(title, message, actions)
        elif self.system == "Darwin":
            self._show_macos_notification(title, message, actions)

    def _show_windows_notification(self, title, message, actions):
        if self.notification_method == "winotify":
            from winotify import Notification, audio

            toast = Notification(
                app_id="EyeBreakReminder",
                title=title,
                msg=message,
                duration="short",
            )

            toast.add_actions(label="Done", launch="action:done")
            toast.add_actions(label="Snooze 5 min", launch="action:snooze")

            toast.set_audio(audio.Default, loop=False)
            toast.show()

        elif self.notification_method == "win10toast":
            self.toaster.show_toast(
                title,
                message,
                duration=10,
                threaded=True,
                callback_on_click=self._notification_callback,
            )

        elif self.notification_method == "plyer":
            import plyer

            plyer.notification.notify(title=title, message=message, timeout=10)

        threading.Timer(30.0, self._auto_dismiss).start()

    def _show_macos_notification(self, title, message, actions):
        if self.notification_method == "pync":
            import pync

            pync.notify(
                message,
                title=title,
                subtitle="20-20-20 Rule Reminder",
                open="eyebreak://done",
                actions={"Done": "eyebreak://done", "Snooze": "eyebreak://snooze"},
                sound="default",
            )

        elif self.notification_method == "plyer":
            import plyer
            import subprocess

            plyer.notification.notify(title=title, message=message, timeout=10)

        threading.Timer(30.0, self._auto_dismiss).start()

    def _notification_callback(self):
        self.dismiss_reminder()

    def _auto_dismiss(self):
        self.is_reminder_active = False

    def dismiss_reminder(self):
        self.is_reminder_active = False

    def snooze_reminder(self):
        self.dismiss_reminder()
        threading.Timer(self.snooze_minutes * 60, self._show_break_reminder).start()

    def _show_break_reminder(self):
        title = "👁️ Eye Break Time!"
        message = "Look at something 20 feet away for 20 seconds (20-20-20 rule)"
        self.show_notification(title, message)

    def start_timer(self):
        def timer_loop():
            while self.should_run:
                time.sleep(self.interval_minutes * 60)
                if self.should_run:
                    self._show_break_reminder()

        timer_thread = threading.Thread(target=timer_loop, daemon=True)
        timer_thread.start()

    def run(self):
        print(f"Eye Break Reminder started on {self.system}!")
        print(
            f"Will remind you every {self.interval_minutes} minutes to take an eye break."
        )
        print("Press Ctrl+C to quit.")

        self.start_timer()

        try:
            while self.should_run:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down Eye Break Reminder...")
            self.should_run = False
    
    def _signal_show_reminder(self, signum, frame):
        """Signal handler for SIGUSR1 - show immediate reminder"""
        print("Received signal to show reminder")
        # Force reset active state and show reminder
        self.is_reminder_active = False
        self._show_break_reminder()
    
    def _signal_shutdown(self, signum, frame):
        """Signal handler for SIGTERM - graceful shutdown"""
        print("Received shutdown signal")
        self.should_run = False


class SimpleEyeBreakReminder:
    def __init__(self, interval_minutes=20):
        try:
            import plyer

            self.plyer = plyer
        except ImportError:
            print("Please install plyer: pip install plyer")
            sys.exit(1)

        self.is_active = False
        self.should_run = True
        self.interval_minutes = interval_minutes
        
        # Set up signal handlers
        signal.signal(signal.SIGUSR1, self._signal_show_reminder)
        signal.signal(signal.SIGTERM, self._signal_shutdown)

    def show_reminder(self):
        if self.is_active:
            return

        self.is_active = True

        self.plyer.notification.notify(
            title="👁️ Eye Break Time!",
            message="Look at something 20 feet away for 20 seconds",
            app_name="Eye Break Reminder",
            timeout=15,
        )

        threading.Timer(30.0, self._reset).start()

    def _reset(self):
        self.is_active = False

    def run(self):
        print("Simple Eye Break Reminder started!")
        print(f"Will remind you every {self.interval_minutes} minutes.")
        print("Press Ctrl+C to quit.")

        try:
            while self.should_run:
                time.sleep(self.interval_minutes * 60)
                if self.should_run and not self.is_active:
                    self.show_reminder()
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.should_run = False
    
    def _signal_show_reminder(self, signum, frame):
        """Signal handler for SIGUSR1 - show immediate reminder"""
        print("Received signal to show reminder")
        # Force reset active state and show reminder
        self.is_active = False
        self.show_reminder()
    
    def _signal_shutdown(self, signum, frame):
        """Signal handler for SIGTERM - graceful shutdown"""
        print("Received shutdown signal")
        self.should_run = False
