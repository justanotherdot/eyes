import pytest
import sys
from unittest.mock import patch, MagicMock
from eyes.cli import main

def test_help_output():
    """Test that --help works without errors."""
    with patch.object(sys, 'argv', ['eyes', '--help']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

def test_version_output():
    """Test that --version works without errors."""
    with patch.object(sys, 'argv', ['eyes', '--version']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

def test_invalid_interval():
    """Test that invalid interval values are rejected."""
    with patch.object(sys, 'argv', ['eyes', '-i', '0']):
        with pytest.raises(SystemExit) as exc_info:
            main() 
        assert exc_info.value.code == 1

def test_invalid_snooze():
    """Test that invalid snooze values are rejected."""
    with patch.object(sys, 'argv', ['eyes', '-s', '0']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1