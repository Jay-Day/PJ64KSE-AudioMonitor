"""
Project64KSE Audio Buffer Monitor - BACKGROUND VERSION
This script runs in the background and automatically fixes the audio buffer whenever you load a ROM
"""

import time
import pyautogui
import psutil
from datetime import datetime

# Configuration
PROCESS_NAME = "Project64KSE.exe"
CHECK_INTERVAL = 2  # Check every 2 seconds

# PyAutoGUI settings
pyautogui.PAUSE = 0.05  # Reduced from 0.1 for faster execution
pyautogui.FAILSAFE = True

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def find_process():
    """Find if Project64KSE is running"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == PROCESS_NAME:
            return proc
    return None

def get_window_title(process_pid=None):
    """Get the current window title of Project64KSE
    If process_pid is provided, only return title for windows belonging to that process
    """
    try:
        import win32process
        import win32gui

        def callback(hwnd, titles):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                title = win32gui.GetWindowText(hwnd)
                if "Project64" in title:
                    titles.append((pid, title, hwnd))

        titles = []
        win32gui.EnumWindows(callback, titles)

        # If we're filtering by PID, only return that one
        if process_pid:
            for pid, title, hwnd in titles:
                if pid == process_pid:
                    return title
        # Otherwise return the first Project64 window
        elif titles:
            return titles[0][1]

    except ImportError:
        # Fallback if win32 modules not available
        try:
            windows = pyautogui.getWindowsWithTitle("Project64")
            for window in windows:
                if "Project64" in window.title:
                    return window.title
        except:
            pass
    except Exception as e:
        pass
    return None

def activate_window():
    """Activate the emulator window"""
    try:
        windows = pyautogui.getWindowsWithTitle("Project64")
        if windows:
            window = windows[0]
            window.activate()
            time.sleep(0.15)  # Reduced from 0.3
            return True
    except:
        pass
    return False

def fix_audio_buffer():
    """Apply the audio buffer fix"""
    log("🔧 Applying audio buffer fix...")

    if not activate_window():
        log("  ⚠ Could not activate window")
        return False

    try:
        # Navigate to audio settings: Alt+O -> DOWN (3x) -> ENTER
        pyautogui.hotkey('alt', 'o')
        time.sleep(0.15)  # Reduced from 0.3
        pyautogui.press('down', presses=3, interval=0.1)  # Reduced from 0.3
        time.sleep(0.1)  # Reduced from 0.3
        pyautogui.press('enter')
        time.sleep(0.4)  # Reduced from 0.8

        # Navigate to buffer slider: TAB (2x)
        pyautogui.press('tab', presses=2, interval=0.1)  # Reduced from 0.2
        time.sleep(0.1)  # Reduced from 0.3

        # Set slider to second tick: HOME then RIGHT
        pyautogui.press('home')
        time.sleep(0.1)  # Reduced from 0.2
        pyautogui.press('right')
        time.sleep(0.1)  # Reduced from 0.2

        # Save settings: ENTER
        pyautogui.press('enter')
        time.sleep(0.2)  # Reduced from 0.5

        log("  ✓ Audio buffer fixed!")
        return True
    except Exception as e:
        log(f"  ✗ Error: {e}")
        return False

def is_rom_loaded(title):
    """Check if the window title indicates a ROM is loaded"""
    if not title:
        return False

    # Ignore netplay-related titles (check the entire title, not just after " - ")
    title_lower = title.lower()
    netplay_keywords = ["netplay", "kaillera", "connected to", "lobby"]
    if any(keyword in title_lower for keyword in netplay_keywords):
        return False

    # ROM is loaded if title contains " - " and something after it
    if " - " in title:
        rom_name = title.split(" - ", 1)[1].strip()

        # Ignore common non-ROM window titles
        ignored_titles = ["File Explorer", "Desktop", "Task Manager", "Control Panel"]
        if rom_name in ignored_titles:
            return False

        # Make sure there's actually a ROM name (not just empty or version info)
        if rom_name and not rom_name.startswith("v") and len(rom_name) > 3:
            return True

    return False

def get_rom_name(title):
    """Extract ROM name from window title"""
    if " - " in title:
        return title.split(" - ", 1)[1].strip()
    return None

def monitor_rom_loading():
    """Monitor for ROM loading and automatically fix audio"""
    log("="*60)
    log("Project64KSE Audio Buffer Monitor - RUNNING")
    log("="*60)
    log("This script will automatically fix the audio buffer when you load a ROM")
    log("Press Ctrl+C to stop monitoring")
    log("="*60)

    last_title = None
    last_rom_state = False  # Track if a ROM was loaded last check
    monitored_pid = None  # Track the PID of the main emulator process
    netplay_detected_recently = False  # Track if we saw netplay window recently

    while True:
        try:
            # Check if Project64KSE is running
            process = find_process()
            if not process:
                if last_title is not None:
                    log("Project64KSE closed")
                    last_title = None
                    last_rom_state = False
                    monitored_pid = None
                    netplay_detected_recently = False
                time.sleep(CHECK_INTERVAL)
                continue

            # Set the PID we're monitoring (only the main process)
            if monitored_pid is None:
                monitored_pid = process.pid

            # Get current window title - ONLY from the main process PID
            current_title = get_window_title(monitored_pid)

            if current_title is None:
                time.sleep(CHECK_INTERVAL)
                continue

            # Check if this title is netplay-related
            title_lower = current_title.lower()
            netplay_keywords = ["netplay", "kaillera", "connected to", "lobby"]
            is_netplay_title = any(keyword in title_lower for keyword in netplay_keywords)

            # If we detect netplay, flag it
            if is_netplay_title:
                netplay_detected_recently = True

            # Check if ROM is currently loaded
            current_rom_state = is_rom_loaded(current_title)

            # First time detecting the window
            if last_title is None:
                log(f"Detected Project64KSE")
                last_title = current_title
                last_rom_state = current_rom_state

                # Don't mention ROM or auto-fix on startup - just start monitoring
                if current_rom_state:
                    log("  ⏸ Monitoring... waiting for ROM to be loaded...")
                else:
                    log("  ⏸ Monitoring... waiting for ROM to be loaded...")

            # Detect ROM loading: transitioned from NO ROM to ROM LOADED
            elif not last_rom_state and current_rom_state:
                # Skip if we recently detected netplay
                if netplay_detected_recently:
                    netplay_detected_recently = False  # Reset the flag
                else:
                    rom_name = get_rom_name(current_title)
                    log(f"📀 ROM loaded: {rom_name}")

                    # Wait a moment for ROM to fully initialize
                    time.sleep(1)  # Reduced from 2

                    # Apply the fix
                    fix_audio_buffer()

            # Detect title change while ROM is still loaded (different ROM)
            elif last_rom_state and current_rom_state and current_title != last_title:
                rom_name = get_rom_name(current_title)
                log(f"📀 ROM changed: {rom_name}")

                # Wait a moment for ROM to fully initialize
                time.sleep(1)  # Reduced from 2

                # Apply the fix
                fix_audio_buffer()

            # Update state
            last_title = current_title
            last_rom_state = current_rom_state

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            log("\n👋 Monitoring stopped by user")
            break
        except Exception as e:
            log(f"⚠ Error in monitoring loop: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        monitor_rom_loading()
    except Exception as e:
        log(f"✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()

    print("\nPress Enter to exit...")
    input()
