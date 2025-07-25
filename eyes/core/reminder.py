import time
import threading
import signal
import abc


class BaseReminder(abc.ABC):
    """Base class for eye break reminders with common functionality"""
    
    def __init__(self, interval_minutes=20):
        self.interval_minutes = interval_minutes
        self.should_run = True
        self.is_active = False
        
        print(f"Reminder interval: {interval_minutes} minutes")
        
        # Set up signal handlers for IPC control
        signal.signal(signal.SIGUSR1, self._signal_show_reminder)
        signal.signal(signal.SIGTERM, self._signal_shutdown)
    
    @abc.abstractmethod
    def show_notification(self, title, message, timeout=None):
        """Platform-specific notification implementation"""
        pass
    
    def show_reminder(self):
        """Show eye break reminder notification"""
        if self.is_active:
            return
        
        self.is_active = True
        self.show_notification(
            "👁️ Eye Break Time!",
            "Look at something 20 feet away for 20 seconds (20-20-20 rule)",
            timeout=30
        )
        
        # Reset active state after timeout
        threading.Timer(30.0, self._reset_active).start()
    
    def _reset_active(self):
        """Reset the active state"""
        self.is_active = False
    
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
    
    def run(self):
        """Main reminder loop"""
        print("Eye Break Reminder started!")
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


class AdvancedReminder(BaseReminder):
    """Advanced reminder with snooze functionality"""
    
    def __init__(self, interval_minutes=20, snooze_minutes=5):
        super().__init__(interval_minutes)
        self.snooze_minutes = snooze_minutes
        self.is_reminder_active = False
        
        print(f"Snooze duration: {snooze_minutes} minutes")
    
    @abc.abstractmethod
    def show_reminder_with_actions(self, title, message, actions):
        """Platform-specific reminder with action buttons"""
        pass
    
    def show_reminder(self):
        """Show advanced reminder with snooze option"""
        if self.is_reminder_active:
            return
            
        self.is_reminder_active = True
        self.show_reminder_with_actions(
            "👁️ Eye Break Time!",
            "Look at something 20 feet away for 20 seconds",
            ["Take Break", "Snooze 5min"]
        )
    
    def handle_reminder_action(self, action):
        """Handle user action from reminder"""
        self.is_reminder_active = False
        
        if action == "snooze":
            print(f"Reminder snoozed for {self.snooze_minutes} minutes")
            threading.Timer(self.snooze_minutes * 60, self.show_reminder).start()
        else:
            print("Break acknowledged")
    
    def run(self):
        """Main reminder loop for advanced reminder"""
        print("Advanced Eye Break Reminder started!")
        print(f"Will remind you every {self.interval_minutes} minutes to take an eye break.")
        print("Press Ctrl+C to quit.")
        
        # Start timer in background thread
        timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        timer_thread.start()
        
        try:
            while self.should_run:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down Eye Break Reminder...")
            self.should_run = False
    
    def _timer_loop(self):
        """Background timer loop"""
        while self.should_run:
            time.sleep(self.interval_minutes * 60)
            if self.should_run:
                self.show_reminder()