import pytest
import platform
from unittest.mock import patch, MagicMock

def test_simple_reminder_init():
    """Test SimpleEyeBreakReminder initialization."""
    with patch('plyer.notification'):
        from eyes.reminder import SimpleEyeBreakReminder
        reminder = SimpleEyeBreakReminder(interval_minutes=30)
        assert reminder.interval_minutes == 30
        assert reminder.is_active is False
        assert reminder.should_run is True

def test_reminder_reset():
    """Test that reminder resets properly."""
    with patch('plyer.notification'):
        from eyes.reminder import SimpleEyeBreakReminder
        reminder = SimpleEyeBreakReminder()
        reminder.is_active = True
        reminder._reset()
        assert reminder.is_active is False

@patch('threading.Timer')
@patch('plyer.notification')
def test_show_reminder(mock_plyer, mock_timer):
    """Test show_reminder functionality."""
    from eyes.reminder import SimpleEyeBreakReminder
    
    reminder = SimpleEyeBreakReminder()
    
    # Mock the notification
    mock_plyer.notify = MagicMock()
    
    reminder.show_reminder()
    
    # Check notification was called
    mock_plyer.notify.assert_called_once()
    assert reminder.is_active is True
    
    # Check timer was started
    mock_timer.assert_called_once_with(30.0, reminder._reset)

def test_show_reminder_when_active():
    """Test that show_reminder returns early when already active."""
    with patch('plyer.notification'):
        from eyes.reminder import SimpleEyeBreakReminder
        reminder = SimpleEyeBreakReminder()
        reminder.is_active = True
        
        with patch('threading.Timer') as mock_timer:
            reminder.show_reminder()
            # Timer should not be called if already active
            mock_timer.assert_not_called()