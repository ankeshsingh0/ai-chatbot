#!/usr/bin/env python
"""List available Gemini models for the configured API key."""

import sys
sys.path.insert(0, '.')

from config.settings import Config
import google.generativeai as genai

genai.configure(api_key=Config.GEMINI_API_KEY)

print("🔍 Available models for your API key:")
print()

for model in genai.list_models():
    supported_methods = model.supported_generation_methods
    if 'generateContent' in supported_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Supported: {supported_methods}")
        print()
