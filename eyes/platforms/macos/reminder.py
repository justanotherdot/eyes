import sys
from ...core.reminder import BaseReminder, AdvancedReminder


class MacOSReminder(BaseReminder):
    """Simple macOS reminder using plyer"""
    
    def __init__(self, interval_minutes=20):
        super().__init__(interval_minutes)
        
        try:
            import plyer
            self.plyer = plyer
        except ImportError:
            print("Please install plyer: pip install plyer")
            sys.exit(1)
    
    def show_notification(self, title, message, timeout=None):
        """Show notification using plyer"""
        self.plyer.notification.notify(
            title=title,
            message=message,
            timeout=timeout or 10
        )


class MacOSAdvancedReminder(AdvancedReminder):
    """Advanced macOS reminder with native notifications and action buttons"""
    
    def __init__(self, interval_minutes=20, snooze_minutes=5):
        super().__init__(interval_minutes, snooze_minutes)
        
        # Try to set up native macOS notifications
        try:
            import pync
            self.pync = pync
            self.notification_method = "pync"
            print("Using native macOS notifications")
        except ImportError:
            try:
                import plyer
                self.plyer = plyer
                self.notification_method = "plyer"
                print("Using plyer notifications (no action buttons)")
            except ImportError:
                print("Please install notification support:")
                print("pip install pync  # for native macOS notifications")
                print("or: pip install plyer  # for basic notifications")
                sys.exit(1)
    
    def show_notification(self, title, message, timeout=None):
        """Show basic notification"""
        if self.notification_method == "pync":
            self.pync.notify(message, title=title)
        else:
            self.plyer.notification.notify(
                title=title,
                message=message,
                timeout=timeout or 10
            )
    
    def show_reminder_with_actions(self, title, message, actions):
        """Show reminder with action buttons (macOS specific)"""
        if self.notification_method == "pync":
            # Use pync with action buttons
            self.pync.notify(
                message,
                title=title,
                actions=actions,
                activate="com.apple.Terminal"  # Bring terminal to front when clicked
            )
        else:
            # Fallback to basic notification
            self.show_notification(title, message)
            # Auto-acknowledge after timeout since we can't handle actions
            import threading
            threading.Timer(30.0, lambda: self.handle_reminder_action("acknowledged")).start()


# Factory function to create appropriate reminder type
def create_reminder(advanced=False, interval_minutes=20, snooze_minutes=5):
    """Create appropriate reminder for macOS"""
    if advanced:
        return MacOSAdvancedReminder(interval_minutes, snooze_minutes)
    else:
        return MacOSReminder(interval_minutes)