@echo off
echo ============================================================
echo Project64KSE Audio Buffer Auto-Fixer - Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

echo Installing required packages...
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo Setup complete!
    echo ============================================================
    echo.
    echo To start the monitor, run: python audio_monitor.py
    echo Or simply double-click audio_monitor.py
    echo.
) else (
    echo.
    echo ============================================================
    echo ERROR: Installation failed
    echo ============================================================
    echo.
    echo Please check the error messages above
    echo.
)

pause
