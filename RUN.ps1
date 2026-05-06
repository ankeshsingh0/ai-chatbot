# ═══════════════════════════════════════════════════════════════
# NeuralChat — PowerShell Run Script
# ═══════════════════════════════════════════════════════════════
# Usage: .\RUN.ps1

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          🤖 NeuralChat AI Chatbot — Starting Server           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path ".\.venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Run: python -m venv .venv"
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "⚙️  Activating Python environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Navigate to server
Set-Location server

# Check dependencies
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import google.generativeai" 2>&1 | Out-Null
} catch {
    Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start server
Write-Host ""
Write-Host "🚀 Starting Flask server..." -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "Server running at: http://localhost:5000" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

python app.py

Read-Host "Press Enter to exit"
