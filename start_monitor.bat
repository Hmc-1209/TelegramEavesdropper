@echo off
chcp 65001 >nul
echo ================================================
echo    Telegram Monitor
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Python not found!
    echo Please install Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo [Check] Checking dependencies...
pip show telethon >nul 2>&1
if %errorlevel% neq 0 (
    echo [Install] Installing Telethon...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [Error] Installation failed!
        pause
        exit /b 1
    )
    echo [Done] Dependencies installed successfully
    echo.
)

REM Run the monitor program
echo [Start] Starting Telegram Monitor...
echo.
python telegram_monitor.py

REM Pause to view messages if program ends
echo.
echo ================================================
pause
