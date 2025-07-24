#!/usr/bin/env python3
"""Build script to create standalone executables using PyInstaller."""

import subprocess
import platform
import sys
from pathlib import Path

def build_executable():
    """Build standalone executable for current platform."""
    system = platform.system()
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--console",  # Console application
        "--name", "eyes",
        "--clean",  # Clean build
        "eyes/cli.py"
    ]
    
    # Platform-specific options
    if system == "Windows":
        cmd.extend([
            "--icon", "NONE",  # No icon for now
            "--add-data", "eyes;eyes"
        ])
    elif system == "Darwin":
        cmd.extend([
            "--add-data", "eyes:eyes"
        ])
    
    # Hidden imports for notification libraries
    cmd.extend([
        "--hidden-import", "plyer.platforms.win.notification",
        "--hidden-import", "plyer.platforms.macosx.notification",
        "--hidden-import", "winotify",
        "--hidden-import", "win10toast",
        "--hidden-import", "pync"
    ])
    
    print(f"Building for {system}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        
        # Show output location
        dist_dir = Path("dist")
        if system == "Windows":
            exe_name = "eyes.exe"
        else:
            exe_name = "eyes"
            
        exe_path = dist_dir / exe_name
        if exe_path.exists():
            print(f"Executable created: {exe_path.absolute()}")
            print(f"Size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()