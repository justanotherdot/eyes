import rumps
import threading
import time

class EyesMenuBarApp(rumps.App):
    def __init__(self):
        super().__init__("👁️", title="👁️")
        self.menu = [
            "Start",
            rumps.separator,
            "Settings",
            "Test Notification",
            rumps.separator,
        ]
        
        self.reminder = None
        self.timer_thread = None
        self.is_running = False
        self.interval = 20  # Default interval
        
    @rumps.clicked("Start")
    def start_stop(self, _):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        """Start the eye break timer"""
        self.is_running = True
        self.menu["Start"].title = "Stop"
        self.title = "👁️ On"
        
        # Create reminder instance
        from .reminder import SimpleEyeBreakReminder
        self.reminder = SimpleEyeBreakReminder(interval_minutes=self.interval)
        
        # Start timer in background thread
        self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self.timer_thread.start()
        
        rumps.notification("Eyes", "Eye break reminder started", f"Will remind every {self.interval} minutes")
    
    def stop_timer(self):
        """Stop the eye break timer"""
        self.is_running = False
        self.menu["Start"].title = "Start"
        self.title = "👁️"
        
        if self.reminder:
            self.reminder.should_run = False
            self.reminder = None
            
        rumps.notification("Eyes", "Eye break reminder stopped", "")
    
    def _timer_loop(self):
        """Background timer loop"""
        while self.is_running and self.reminder and self.reminder.should_run:
            time.sleep(self.interval * 60)  # Convert minutes to seconds
            if self.is_running and self.reminder and not self.reminder.is_active:
                self.reminder.show_reminder()
    
    @rumps.clicked("Test Notification")
    def test_notification(self, _):
        """Test notification"""
        try:
            if not self.reminder:
                from .reminder import SimpleEyeBreakReminder
                self.reminder = SimpleEyeBreakReminder(interval_minutes=self.interval)
            self.reminder.show_reminder()
        except Exception as e:
            rumps.alert("Notification Error", f"Failed to show notification: {e}")
    
    @rumps.clicked("Settings")
    def settings(self, _):
        """Show settings dialog"""
        response = rumps.Window(
            message="Set reminder interval:",
            title="Eyes Settings",
            default_text=str(self.interval),
            ok="Save",
            cancel="Cancel",
            dimensions=(200, 20)
        ).run()
        
        if response.clicked and response.text:
            try:
                new_interval = int(response.text)
                if new_interval > 0:
                    self.interval = new_interval
                    rumps.notification("Eyes", "Settings updated", f"Interval set to {new_interval} minutes")
                    
                    # Restart timer if running
                    if self.is_running:
                        self.stop_timer()
                        self.start_timer()
                else:
                    rumps.alert("Invalid interval", "Please enter a positive number")
            except ValueError:
                rumps.alert("Invalid interval", "Please enter a valid number")

def launch_menu_bar_app():
    """Launch the menu bar application"""
    try:
        print("Starting menu bar app...")
        app = EyesMenuBarApp()
        print("App created, starting run loop...")
        app.run()
    except Exception as e:
        print(f"Error launching menu bar app: {e}")
        import traceback
        traceback.print_exc()