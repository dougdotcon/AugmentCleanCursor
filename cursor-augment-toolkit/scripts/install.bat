@echo off
echo Starting Augment VIP installation...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run the Python installer
python install.py %*

if %ERRORLEVEL% NEQ 0 (
    echo Installation failed.
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo You can now use Augment VIP with the commands shown above.
echo.
pause
