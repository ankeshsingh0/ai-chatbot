# ✅ NeuralChat — Verification Checklist

Use this checklist to verify your setup is complete and working.

---

## 🔍 File Structure Check

- [ ] Project folder at: `c:\Users\anurag kumar\OneDrive\chukachi\ai-chatbot`
- [ ] `RUN.bat` exists (for easy launch)
- [ ] `RUN.ps1` exists (PowerShell alternative)
- [ ] `server/.env` exists (with API key)
- [ ] `server/.env.example` exists (template)
- [ ] `.venv/` folder exists (Python environment)
- [ ] `client/index.html` exists
- [ ] `server/app.py` exists

---

## 🐍 Python Environment Check

```bash
# Run these commands
.venv\Scripts\activate
python --version
```

Expected: Python 3.12.0 or higher ✅

---

## 📦 Dependencies Check

```bash
.venv\Scripts\activate
python -c "import flask; import google.generativeai; print('All dependencies OK')"
```

Expected: "All dependencies OK" ✅

---

## 🔑 API Key Check

```bash
cd server
python -c "from config.settings import Config; print(f'API Key set: {bool(Config.GEMINI_API_KEY)}'); print(f'Model: {Config.GEMINI_MODEL}')"
```

Expected:
```
API Key set: True
Model: gemini-2.5-flash
```
✅

---

## 🚀 Server Start Check

```bash
# From project root
RUN.bat
```

OR

```bash
.venv\Scripts\activate
cd server
python app.py
```

Expected output:
```
⠙ Loading environment...
✅ Config loaded
🚀 NeuralChat server running on http://localhost:5000
```
✅

---

## 🌐 Frontend Check

1. Open browser: **http://localhost:5000**
2. You should see:
   - ✅ Chat interface with message input
   - ✅ Title: "NeuralChat"
   - ✅ "Powered by Google Gemini" text
   - ✅ Send button active

---

## 💬 Chat Functionality Check

1. Type in the chat box: "hello"
2. Click Send
3. Expected: AI responds within 3 seconds

---

## 🔧 Configuration Check

File: `server/.env`

- [ ] `GEMINI_API_KEY` is set
- [ ] `AI_PROVIDER=gemini` is set
- [ ] `GEMINI_MODEL=gemini-2.5-flash` is set
- [ ] `PORT=5000` (or your custom port)

---

## 📝 Git Check (Before Committing)

```bash
git status
```

Make sure:
- ❌ `.env` is NOT listed (should be ignored)
- ❌ `.venv/` is NOT listed (should be ignored)
- ✅ Only source files and docs are shown

---

## ✨ Everything Working?

If all checks pass, you're ready!

```bash
RUN.bat  # Launch anytime with this
```

---

## 🆘 Troubleshooting

| Check Failed? | Try This |
|---|---|
| Python version wrong | Install Python 3.10+ from python.org |
| Dependencies missing | Run `pip install -r server/requirements.txt` |
| API key not set | Check `server/.env` exists with GEMINI_API_KEY |
| Server won't start | Try `python -m flask --app server.app run` |
| Chat not responding | Verify GEMINI_API_KEY is valid (test on makersuite.google.com) |
| Port 5000 in use | Change PORT in `server/.env` to 5001, 5002, etc. |

---

**Last Checked:** February 27, 2026 ✅
