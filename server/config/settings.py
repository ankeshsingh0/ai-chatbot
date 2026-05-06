"""
NeuralChat — Configuration Settings
─────────────────────────────────────
All config values loaded from environment variables.
Copy .env.example → .env and fill in your values.
"""

import sys
import os
from dotenv import load_dotenv

# Load .env file from the server directory (absolute path)
server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(server_dir, '.env')
loaded = load_dotenv(dotenv_path=env_path, override=True)

# Debug: print loaded configuration
print(f"🔧 Config loaded from: {env_path}")
print(f"📂 File exists: {os.path.exists(env_path)}")
print(f"✓ AI_PROVIDER env var: {os.getenv('AI_PROVIDER', 'NOT SET')}")


class Config:
    # ── Server ──
    PORT:  str = os.getenv('PORT', '5000')
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')

    # ── Database ──
    MONGO_URI:  str = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DB_NAME:    str = os.getenv('DB_NAME', 'neuralchat')

    # ── AI Provider — choose 'openai' or 'gemini' ──
    AI_PROVIDER: str = os.getenv('AI_PROVIDER', 'openai')

    # ── OpenAI ──
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL:   str = os.getenv('OPENAI_MODEL',   'gpt-3.5-turbo')

    # ── Google Gemini ──
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL:   str = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

    # ── Chat limits ──
    MAX_MESSAGE_LENGTH:  int = int(os.getenv('MAX_MESSAGE_LENGTH', '2000'))
    MAX_HISTORY_CONTEXT: int = int(os.getenv('MAX_HISTORY_CONTEXT', '20'))
    MAX_HISTORY_STORED:  int = int(os.getenv('MAX_HISTORY_STORED', '100'))

    # ── System Prompt — defines the AI's personality ──
    SYSTEM_PROMPT: str = os.getenv('SYSTEM_PROMPT', """
You are NeuralChat, an expert AI assistant specializing in programming and academic study.

Your personality:
- Friendly, concise, and encouraging
- Explain complex topics in simple, clear language
- Always provide code examples when discussing programming
- Format code using proper markdown code blocks with language tags
- Use bullet points and headings for structured explanations
- Acknowledge when you're unsure and suggest alternatives
- Encourage best practices and clean code habits

Domains you excel at:
- Programming (Python, JavaScript, TypeScript, Java, C++, Go, Rust, etc.)
- Web development (HTML, CSS, React, Node.js, Flask, Django)
- Data structures & algorithms
- System design & architecture
- Mathematics and science
- General academic study skills

Always respond in Markdown format for rich text rendering.
""".strip())
