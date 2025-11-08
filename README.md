# Project64KSE Audio Buffer Auto-Fixer

Automatically fixes the audio buffer setting in Project64KSE whenever you load a ROM.

## Problem

Project64KSE resets the audio buffer setting every time you load a ROM, causing audio stuttering. This script automatically sets the audio buffer to the second tick (optimal setting) whenever you load a new ROM.

## Features

- 🎮 Automatically detects when you load a ROM
- 🔧 Instantly applies the correct audio buffer setting
- 🚫 Ignores netplay windows and other false triggers
- 💻 Runs quietly in the background
- 🔁 Works for every ROM you load

## Requirements

- Windows (uses Windows-specific libraries)
- Python 3.7 or higher
- Project64KSE emulator

## Installation

### Easy Way (Windows)

1. **Install Python** (if you don't have it)
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, **check "Add Python to PATH"**

2. **Download this script**
   - Download as ZIP or clone the repository
   - Extract to a folder

3. **Double-click `setup.bat`**
   - This will automatically install all required packages
   - Wait for it to finish

### Manual Way

1. **Install Python** (if you don't have it)
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Download this script**
   ```bash
   git clone https://github.com/yourusername/project64kse-audio-fixer.git
   cd project64kse-audio-fixer
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the monitor script:**
   ```bash
   python audio_monitor.py
   ```

   Or simply double-click `audio_monitor.py` in File Explorer

2. **Launch Project64KSE** and load any ROM

3. **The script will automatically fix the audio buffer!**

4. **To stop monitoring:** Press `Ctrl+C` or close the window

## Configuration

By default, the script:
- Sets the audio buffer to the **second tick** on the slider
- Monitors every **2 seconds** for changes

To change these settings, edit the variables at the top of `audio_monitor.py`:

```python
CHECK_INTERVAL = 2  # How often to check (in seconds)
```

To change which tick the slider is set to, modify the audio fix section:
```python
# Currently: HOME then RIGHT arrow (second tick)
pyautogui.press('home')
pyautogui.press('right')  # Change to 'right', presses=2 for third tick, etc.
```

## How It Works

The script uses a continuous monitoring loop to detect when you load a ROM and automatically applies the audio buffer fix. Here's exactly what happens:

### Monitoring Phase

1. **Process Detection**: Every 2 seconds, the script checks if `Project64KSE.exe` is running using `psutil`

2. **Window Tracking**: Once detected, the script captures the main emulator window's PID (process ID) to monitor only the primary window, ignoring child windows

3. **Title Monitoring**: The script reads the window title using Windows APIs (`win32gui`) to detect ROM loading

4. **ROM Detection Logic**:
   - A ROM is considered "loaded" when the window title changes from the base emulator title to include a ROM name (format: `Project64KSE - [ROM Name]`)
   - The script specifically **ignores netplay windows** by checking for keywords like "netplay", "kaillera", "connected to", or "lobby" in the title
   - It tracks state transitions: from "no ROM" to "ROM loaded" or from "ROM A" to "ROM B"

### Auto-Fix Phase

When a ROM load is detected:

1. **Wait Period**: Waits 2 seconds for the ROM to fully initialize

2. **Window Activation**: Brings the Project64KSE window to the foreground using `pyautogui`

3. **Menu Navigation**:
   - Presses `Alt+O` to open the Options menu
   - Presses `Down` 3 times to navigate to "Configure Audio Plugin"
   - Presses `Enter` to open the audio configuration dialog

4. **Slider Adjustment**:
   - Presses `Tab` twice to focus on the audio buffer slider
   - Presses `Home` to move the slider to the leftmost position
   - Presses `Right` once to move to the second tick (optimal setting)

5. **Save Settings**: Presses `Enter` to save and close the dialog

### Smart Filtering

The script includes several safeguards to prevent false triggers:

- **Netplay Protection**: Detects and ignores netplay-related window titles to avoid interfering during online play
- **PID Filtering**: Only monitors the main emulator process window, not child/popup windows
- **State Tracking**: Uses state machines to detect actual ROM loading transitions, not just any title change
- **Ignored Titles**: Filters out common non-ROM windows like "File Explorer", "Desktop", etc.

## Troubleshooting

**Script doesn't detect ROM loading:**
- Make sure Project64KSE is running
- Check that the window title contains the ROM name

**Audio fix doesn't work:**
- The script assumes default Project64KSE menu layout
- Menu navigation: `Alt+O` → `DOWN` (3x) → `ENTER`
- Buffer slider: `TAB` (2x) from the audio config dialog

**Netplay triggers the fix incorrectly:**
- The script should ignore netplay windows automatically
- If it doesn't, the netplay keywords may need updating

## Notes

- Only works on **Windows** (uses `pywin32` for window management)
- Designed for **Project64KSE** specifically (may not work with other Project64 versions)
- The script must keep running in the background to work

## License

MIT License - Feel free to use and modify!

## Credits

Created to solve the annoying audio buffer reset issue in Project64KSE.
