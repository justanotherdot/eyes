import sys
from ...core.reminder import BaseReminder, AdvancedReminder


class WindowsReminder(BaseReminder):
    """Simple Windows reminder using available notification libraries"""
    
    def __init__(self, interval_minutes=20):
        super().__init__(interval_minutes)
        
        # Try different Windows notification libraries in order of preference
        try:
            import plyer
            self.plyer = plyer
            self.notification_method = "plyer"
            print("Using plyer notifications")
        except ImportError:
            try:
                import win10toast
                self.toaster = win10toast.ToastNotifier()
                self.notification_method = "win10toast"
                print("Using win10toast notifications")
            except ImportError:
                try:
                    from winotify import Notification
                    self.winotify = Notification
                    self.notification_method = "winotify"
                    print("Using winotify notifications")
                except ImportError:
                    print("Please install notification support:")
                    print("pip install winotify")
                    print("or: pip install plyer")
                    print("or: pip install win10toast")
                    sys.exit(1)
    
    def show_notification(self, title, message, timeout=None):
        """Show notification using available Windows library"""
        if self.notification_method == "plyer":
            self.plyer.notification.notify(
                title=title,
                message=message,
                timeout=timeout or 10
            )
        elif self.notification_method == "win10toast":
            self.toaster.show_toast(
                title,
                message,
                duration=timeout or 10,
                threaded=True
            )
        elif self.notification_method == "winotify":
            toast = self.winotify(
                app_id="Eyes",
                title=title,
                msg=message,
                duration="short"
            )
            toast.show()


class WindowsAdvancedReminder(AdvancedReminder):
    """Advanced Windows reminder - same as basic for now"""
    
    def __init__(self, interval_minutes=20, snooze_minutes=5):
        super().__init__(interval_minutes, snooze_minutes)
        
        # Use same notification setup as basic reminder
        reminder = WindowsReminder(interval_minutes)
        self.notification_method = reminder.notification_method
        
        if hasattr(reminder, 'plyer'):
            self.plyer = reminder.plyer
        elif hasattr(reminder, 'toaster'):
            self.toaster = reminder.toaster
        elif hasattr(reminder, 'winotify'):
            self.winotify = reminder.winotify
    
    def show_notification(self, title, message, timeout=None):
        """Show basic notification (same as WindowsReminder)"""
        if self.notification_method == "plyer":
            self.plyer.notification.notify(
                title=title,
                message=message,
                timeout=timeout or 10
            )
        elif self.notification_method == "win10toast":
            self.toaster.show_toast(
                title,
                message,
                duration=timeout or 10,
                threaded=True
            )
        elif self.notification_method == "winotify":
            toast = self.winotify(
                app_id="Eyes",
                title=title,
                msg=message,
                duration="short"
            )
            toast.show()
    
    def show_reminder_with_actions(self, title, message, actions):
        """Show reminder - Windows doesn't support action buttons easily"""
        # Just show basic notification and auto-acknowledge
        self.show_notification(title, message)
        
        # Auto-acknowledge after timeout since Windows doesn't easily support action buttons
        import threading
        threading.Timer(30.0, lambda: self.handle_reminder_action("acknowledged")).start()


# Factory function to create appropriate reminder type
def create_reminder(advanced=False, interval_minutes=20, snooze_minutes=5):
    """Create appropriate reminder for Windows"""
    if advanced:
        return WindowsAdvancedReminder(interval_minutes, snooze_minutes)
    else:
        return WindowsReminder(interval_minutes)