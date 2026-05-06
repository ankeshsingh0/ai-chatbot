# ⬡ NeuralChat — Production AI Chatbot

> A full-stack AI chatbot with ChatGPT-style UI, MongoDB persistence, context-aware conversations, and support for Google Gemini (OpenAI support is commented out).

---

## 📁 Project Structure

```
ai-chatbot/
│
├── client/                     # Frontend (HTML + CSS + JS)
│   ├── index.html              # Main HTML shell
│   ├── css/
│   │   └── style.css           # Full responsive CSS with dark/light themes
│   └── js/
│       └── app.js              # All frontend logic
│
├── server/                     # Backend (Python + Flask)
│   ├── app.py                  # Flask app factory & entry point
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variable template
│   │
│   ├── config/
│   │   └── settings.py         # All config loaded from environment
│   │
│   ├── database/
│   │   └── db.py               # MongoDB connection + init
│   │
│   ├── models/
│   │   └── message_model.py    # CRUD operations for messages
│   │
│   ├── routes/
│   │   ├── chat_routes.py      # POST /chat
│   │   └── history_routes.py   # GET /history, DELETE /clear
│   │
│   └── services/
│       └── ai_service.py       # OpenAI + Gemini abstraction layer
│
├── Procfile                    # For Render/Railway deployment
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

| Tool        | Version   | Install                            |
|-------------|-----------|------------------------------------|
| Python      | 3.10+     | https://python.org                 |
| MongoDB     | 6.0+      | https://mongodb.com/try/download   |
| Git         | Any       | https://git-scm.com                |

---

## 🔧 Step-by-Step Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/neuralchat.git
cd neuralchat
```

### Step 2 — Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
source venv/bin/activate
```

### Step 3 — Install Python Dependencies

```bash
cd server
pip install -r requirements.txt
```

### Step 4 — Add Your API Key

```bash
# Copy the example env file
cp .env.example .env

# Open .env and add your key:
# For OpenAI:
# OPENAI_API_KEY=sk-your-key-here  (not used for Gemini-only)
AI_PROVIDER=openai

# OR for Gemini:
GEMINI_API_KEY=your-key-here
AI_PROVIDER=gemini
```

#### Where to get API keys:

- **OpenAI**: https://platform.openai.com/api-keys → Create new secret key
- **Gemini**: https://makersuite.google.com/app/apikey → Get API key

### Step 5 — Start MongoDB

```bash
# If installed locally:
mongod

# Or use MongoDB Atlas (cloud) — paste the connection string in .env:
MONGO_URI=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/
```

### Step 6 — Run the Backend Server

```bash
# Make sure you're in the server/ directory with venv active
python app.py
```

✅ MongoDB connected → 'neuralchat' database
🚀 NeuralChat server running on http://localhost:5000
```

### Step 7 — Open the Frontend

Simply open `client/index.html` in your browser.

> **No build step required!** It's plain HTML/CSS/JS.

For a local web server (recommended to avoid CORS quirks):
```bash
# Python quick server from the client/ folder:
cd client
python -m http.server 3000
# Open: http://localhost:3000
```

---

## 🔌 API Reference

### `POST /chat`

Send a message and receive an AI response.

**Request:**
```json
{
  "message":  "Explain async/await in JavaScript",
  "username": "Alex"
}
```

**Response:**
```json
{
## ⚡ Quick Start
  "timestamp": "2024-01-15T10:30:00.000Z",
  "saved":     true
}
```

---

### `GET /history?username=Alex`

Retrieve chat history for a user.

**Response:**
```json
{
  "history": [
    {
      "id":        "65a1b2c3d4e5f6a7b8c9d0e1",
      "username":  "Alex",
      "message":   "What is Python?",
      "reply":     "Python is a high-level programming language...",
    }
  ],
  "count": 1
}
```

---

### `DELETE /clear`

Clear all chat history for a user.

**Request:**
```json
```

**Response:**
```json
{
  "message":       "Cleared history for 'Alex'",
  "deleted_count": 12
}
```

---

### `GET /health`

Check server status.

**Response:**
```json
{ "status": "ok", "service": "NeuralChat API" }
```

---

## 🗄️ MongoDB Schema

Collection: `messages`

```json
{
  "_id":        "ObjectId",
  "username":   "string",
  "message":    "string  — user's input",
  "reply":      "string  — AI's response",
  "timestamp":  "datetime",
  "created_at": "datetime"
}
```

**Indexes:**
- `username` — for fast user lookups
- `(username, timestamp)` — compound, for sorted history

---

## 🌟 Features

| Feature                         | Status |
|---------------------------------|--------|
| ChatGPT-style UI                | ✅     |
| Dark / Light mode toggle        | ✅     |
| Typing animation                | ✅     |
| Markdown + code syntax highlight| ✅     |
| Context-aware conversation      | ✅     |
| MongoDB chat persistence        | ✅     |
| Chat history on reload          | ✅     |
| Copy message button             | ✅     |
| Copy code button in code blocks | ✅     |
| Download chat as .txt           | ✅     |
| Clear chat button               | ✅     |
| Voice input (browser API)       | ✅     |
| Character limit + counter       | ✅     |
| Auto-resize textarea            | ✅     |
| Mobile responsive               | ✅     |
| Simple username auth            | ✅     |
| OpenAI GPT integration          | ✅     |
| Google Gemini integration       | ✅     |
| Deployment ready                | ✅     |

---

## ☁️ Deployment

### Deploy Backend to Render (Free Tier)

1. Push code to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Configure:
   - **Root Directory:** `server`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:create_app --bind 0.0.0.0:$PORT`
5. Add Environment Variables (copy from `.env`):
   - `GEMINI_API_KEY` (since only Gemini is used)
   - `MONGO_URI` (use MongoDB Atlas URI)
   - `AI_PROVIDER=gemini`
   - `DEBUG=false`
6. Click **Deploy**

### Deploy Frontend to Netlify

1. Go to https://netlify.com → Add New Site → Deploy manually
2. Drag and drop your `client/` folder
3. Update `CONFIG.API_BASE` in `client/js/app.js`:
   ```js
   const CONFIG = {
     API_BASE: 'https://your-render-app.onrender.com',
     ...
   };
   ```
4. Done! Frontend is live.

### MongoDB Atlas (Free Cloud DB)

1. https://mongodb.com/atlas → Create free cluster
2. Database Access → Add user with password
3. Network Access → Allow from anywhere (`0.0.0.0/0`)
4. Clusters → Connect → Copy connection string
5. Paste into `MONGO_URI` in your environment variables

---

## ⚙️ Configuration Reference

| Variable              | Default              | Description                          |
|-----------------------|----------------------|--------------------------------------|
| `PORT`                | `5000`               | Server port                          |
| `DEBUG`               | `false`              | Flask debug mode                     |
| `MONGO_URI`           | `mongodb://localhost`| MongoDB connection string            |
| `DB_NAME`             | `neuralchat`         | Database name                        |
| `AI_PROVIDER`         | `gemini`             | `gemini` (OpenAI support is disabled) |
| `GEMINI_API_KEY`      | —                    | Your Gemini API key                  |
| `GEMINI_MODEL`        | `gemini-pro`         | Gemini model name                    |
| `MAX_MESSAGE_LENGTH`  | `2000`               | Max chars per message                |
| `MAX_HISTORY_CONTEXT` | `20`                 | Previous messages sent as AI context |
| `SYSTEM_PROMPT`       | (see settings.py)    | AI personality instructions          |

---

## 🏗️ Architecture

```
Browser (client/)
    │
    │ HTTP/REST
    ▼
Flask Server (server/)
    │
    ├─► ai_service.py ──► OpenAI API / Gemini API
    │                           │
    │                      AI Response
    │
    └─► message_model.py ──► MongoDB
                                │
                          Saved Exchange
```

**Request Flow:**
1. User types → JS validates → `POST /chat`
2. Flask receives → validates → fetches recent context from MongoDB
3. Context + message sent to AI provider
4. AI response returned
5. Exchange saved to MongoDB
6. Response sent to browser
7. Markdown rendered, bubble animated in

---

## 🐛 Troubleshooting

**MongoDB connection refused?**
```bash
# Start MongoDB manually:
sudo systemctl start mongod
# or:
mongod --dbpath /data/db
```

**CORS errors?**
- Make sure `flask-cors` is installed
- Check `CONFIG.API_BASE` in `app.js` matches your server URL

**OpenAI quota exceeded?**
- Check usage at https://platform.openai.com/usage
- Downgrade to `gpt-3.5-turbo` (much cheaper)

**Voice input not working?**
- Requires HTTPS in production (browsers block mic on HTTP)
- Works fine on localhost

---

## 📄 License

MIT License — use freely for personal and commercial projects.

---

*Built with ❤️ — NeuralChat*
