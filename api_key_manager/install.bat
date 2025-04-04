@echo off
echo ===================================
echo API Key Manager - Installation
echo ===================================
echo.

echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies! 
    echo Please make sure pip is installed and you have internet access.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Dependencies installed successfully!
echo.
echo ===================================
echo You can now:
echo.
echo 1. Run the application:
echo    python main.py
echo.
echo 2. Build the executable:
echo    python build_exe.py
echo.
echo 3. Configure the application in config.json
echo ===================================
echo.
pause
