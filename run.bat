@echo off
title Supply Chain Transparency - Local Server
echo =======================================================
echo     Supply Chain Transparency for Small Farms
echo =======================================================
echo.
echo Attempting to start a local development server...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python detected.
    echo Starting server at http://localhost:8000...
    echo Press Ctrl+C to stop the server.
    echo.
    start http://localhost:8000
    python -m http.server 8000
    goto :eof
)

:: Check if Node.js (npx) is installed
npx --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Node.js detected.
    echo Starting server...
    echo Press Ctrl+C to stop the server.
    echo.
    npx http-server -p 8000 -o
    goto :eof
)

:: If neither is found
echo [ERROR] Neither Python nor Node.js (npx) was found on your system.
echo.
echo To run this project, you have a few options:
echo 1. Install Python from python.org
echo 2. Install Node.js from nodejs.org
echo 3. Use the "Live Server" extension in Visual Studio Code (Recommended)
echo.
pause
