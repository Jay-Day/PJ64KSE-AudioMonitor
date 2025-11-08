# Project64KSE Audio Buffer Auto-Fixer

Automatically fixes the audio buffer setting in Project64KSE whenever you load a ROM.

![2025-11-08 15-16-23](https://github.com/user-attachments/assets/6153fd65-cd2e-421d-bac2-9119b37fb25c)


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

1. Monitors the Project64KSE process and window title
2. Detects when you load a ROM (window title changes)
3. Waits 2 seconds for the ROM to initialize
4. Navigates to: Options → Configure Audio Plugin
5. Sets the buffer slider to the second tick
6. Saves the settings

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
