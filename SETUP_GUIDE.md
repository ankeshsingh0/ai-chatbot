# 🚀 NeuralChat — Setup & Run Guide

## ✅ Status: Fully Working! 

Your chatbot is **production-ready** and running with:
- ✨ Google Gemini API (latest `gemini-2.5-flash` model)
- 💬 Full context-aware conversations
- 🎨 ChatGPT-style responsive UI
- ⚡ Flask backend with error handling

---

## 🎯 Quick Start (Next Time You Open This Project)

### **Option 1: One-Click Run (Easiest)**
Simply double-click `RUN.bat` in the project root folder.

That's it! The server will start automatically on `http://localhost:5000`

### **Option 2: Manual Run**

```bash
# 1. Activate virtual environment (from project root)
.venv\Scripts\activate

# 2. Go to server directory
cd server

# 3. Start Flask
python app.py

# 4. Open http://localhost:5000 in your browser
```

---

## 🔑 Important: API Key Setup (First Time Only)

You already have your `.env` file configured, but if you reinstall:

1. **Get Google Gemini API Key:**
   - Go to https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2. **Add it to `server/.env`:**
   ```
   GEMINI_API_KEY=your-api-key-here
   AI_PROVIDER=gemini
   GEMINI_MODEL=gemini-2.5-flash
   ```

---

## 📁 Project Structure (Reference)

```
ai-chatbot/
├── RUN.bat                    ← Double-click to start! ⭐
├── client/
│   ├── index.html             ← Frontend UI
│   ├── css/style.css
│   └── js/app.js
├── server/
│   ├── app.py                 ← Main Flask app
│   ├── .env                   ← Your API keys (DO NOT commit!)
│   ├── .env.example           ← Template for .env
│   ├── requirements.txt
│   ├── config/settings.py     ← Configuration loading
│   ├── routes/                ← API endpoints
│   ├── services/ai_service.py ← Gemini integration
│   └── models/                ← Database models
└── README.md
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` when running | Make sure venv is activated: `.venv\Scripts\activate` |
| `GEMINI_API_KEY not found` | Check that `.env` file exists in `server/` folder with correct key |
| Port 5000 already in use | Change `PORT=5000` in `server/.env` to another port like `PORT=5001` |
| Chat returns error | Make sure GEMINI_API_KEY is valid (test at https://makersuite.google.com/app/apikey) |

---

## 🔧 What Was Set Up

✅ **Backend:** Flask 3.0.0 with Python 3.12  
✅ **AI Provider:** Google Gemini API (gemini-2.5-flash)  
✅ **Frontend:** Modern HTML/CSS/JS UI (no build needed)  
✅ **Dependencies:** All installed in `.venv/` virtual environment  

---

## 📝 Next Steps (Optional Enhancements)

- [ ] Set up MongoDB for chat history persistence
- [ ] Add user authentication
- [ ] Deploy to cloud (Render, Heroku, AWS)
- [ ] Add voice input/output
- [ ] Customize system prompt in `server/.env`

---

**Enjoy your AI chatbot! 🤖**
