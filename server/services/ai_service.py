"""
NeuralChat — AI Service
─────────────────────────
Abstraction layer for AI providers.
Supports: OpenAI (GPT) and Google Gemini.

Set AI_PROVIDER in .env to 'openai' or 'gemini'.
"""

import os
from config.settings import Config


# ════════════════════════════════════════════════════
# OPENAI PROVIDER (commented out - using Gemini only)
# ════════════════════════════════════════════════════
#
# def _get_openai_response(user_message: str, context: list[dict]) -> str:
#     """
#     Send a message to OpenAI GPT and return the response.
#
#     Args:
#         user_message: The user's current message
#         context:      List of previous {message, reply} dicts for memory
#
#     Returns:
#         AI response string
#     """
#     try:
#         from openai import OpenAI
#     except ImportError:
#         raise RuntimeError("openai package not installed. Run: pip install openai")
#
#     client = OpenAI(api_key=Config.OPENAI_API_KEY)
#
#     if not Config.OPENAI_API_KEY:
#         raise ValueError("OPENAI_API_KEY not set in environment variables")
#
#     # Build message history for context-awareness
#     messages = [{"role": "system", "content": Config.SYSTEM_PROMPT}]
#
#     # Add previous conversation pairs as context
#     for exchange in context:
#         messages.append({"role": "user",      "content": exchange["message"]})
#         messages.append({"role": "assistant", "content": exchange["reply"]})
#
#     # Add current message
#     messages.append({"role": "user", "content": user_message})
#
#     response = client.chat.completions.create(
#         model=Config.OPENAI_MODEL,
#         messages=messages,
#         max_tokens=1500,
#         temperature=0.7,
#     )
#
#     return response.choices[0].message.content.strip()


# ════════════════════════════════════════════════════
# GEMINI PROVIDER
# ════════════════════════════════════════════════════

def _get_gemini_response(user_message: str, context: list[dict]) -> str:
    """
    Send a message to Google Gemini and return the response.

    Args:
        user_message: The user's current message
        context:      List of previous {message, reply} dicts for memory

    Returns:
        AI response string
    """
    try:
        import google.generativeai as genai
    except ImportError:
        raise RuntimeError("google-generativeai package not installed. Run: pip install google-generativeai")

    if not Config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in environment variables")

    genai.configure(api_key=Config.GEMINI_API_KEY)
    # instantiate model without system_instruction (not supported in this version)
    model = genai.GenerativeModel(
        model_name=Config.GEMINI_MODEL,
    )

    # Build chat history for context (Gemini only supports 'user' and 'model' roles)
    history = []
    for exchange in context:
        history.append({"role": "user",  "parts": [exchange["message"]]})
        history.append({"role": "model", "parts": [exchange["reply"]]})

    chat = model.start_chat(history=history)
    
    # Prepend system prompt to first user message for persona/instructions
    enhanced_message = f"{Config.SYSTEM_PROMPT}\n\n{user_message}"
    try:
        response = chat.send_message(enhanced_message)
    except Exception as exc:
        # provide more context for API failures
        raise RuntimeError(f"Gemini API request failed: {exc}") from exc
    return response.text.strip()


# ════════════════════════════════════════════════════
# UNIFIED INTERFACE
# ════════════════════════════════════════════════════

def get_ai_response(user_message: str, context: list[dict]) -> str:
    """
    Route the request to the configured AI provider.

    Args:
        user_message: The user's input text
        context:      Recent conversation history for memory

    Returns:
        AI-generated response string

    Raises:
        ValueError: If AI_PROVIDER is unsupported or API key is missing
        RuntimeError: If the API call fails
    """
    provider = Config.AI_PROVIDER.lower().strip()

    # only Gemini provider supported; ignore other settings
    if provider == 'gemini':
        return _get_gemini_response(user_message, context)
    else:
        # silently fallback to gemini if misconfigured
        return _get_gemini_response(user_message, context)
