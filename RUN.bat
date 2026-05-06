@echo off
REM ═══════════════════════════════════════════════════════════════
REM NeuralChat — Quick Start Script (Windows)
REM ═════════════════════════════════════════════════════════════════
REM This script activates the virtual environment and runs the server

cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║          🤖 NeuralChat AI Chatbot — Starting Server           ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check if venv exists
if not exist ".venv" (
    echo ❌ Virtual environment not found!
    echo Run: python -m venv .venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo ⚙️  Activating Python environment...
call .venv\Scripts\activate.bat

REM Navigate to server directory
cd server

REM Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import google.generativeai" >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

REM Start the server
echo.
echo 🚀 Starting Flask server...
echo.
echo ═══════════════════════════════════════════════════════════════
echo Server running at: http://localhost:5000
echo ═══════════════════════════════════════════════════════════════
echo.

python app.py

pause
