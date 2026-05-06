"""
NeuralChat — Chat Routes
─────────────────────────
POST /chat  → Send message, get AI response, save to DB
"""

from flask import Blueprint, request, jsonify
from config.settings import Config
from models.message_model import MessageModel
from services.ai_service import get_ai_response
import traceback

# Blueprint for chat routes
chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint.

    Request body (JSON):
        {
            "message":  "user's message text",
            "username": "display name"
        }

    Response (JSON):
        {
            "reply":     "AI's response",
            "timestamp": "ISO timestamp",
            "saved":     true/false (whether saved to DB)
        }
    """

    # ── Parse & Validate Input ──────────────────────
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    message  = data.get('message', '').strip()
    username = data.get('username', 'anonymous').strip()

    # Validate message
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    if len(message) > Config.MAX_MESSAGE_LENGTH:
        return jsonify({
            "error": f"Message too long. Maximum {Config.MAX_MESSAGE_LENGTH} characters allowed."
        }), 400

    # Sanitize username
    if not username:
        username = 'anonymous'
    username = username[:50]  # max 50 chars

    # ── Build Context from History ──────────────────
    # Fetch recent exchanges so AI remembers the conversation
    context = MessageModel.get_context(
        username=username,
        limit=Config.MAX_HISTORY_CONTEXT
    )

    # ── Call AI ─────────────────────────────────────
    try:
        reply = get_ai_response(
            user_message=message,
            context=context,
        )
    except ValueError as e:
        # Config error (missing API key, bad provider)
        print(f"[Chat] Config error: {e}")
        return jsonify({"error": str(e)}), 500

    except RuntimeError as e:
        # Package or network error
        print(f"[Chat] AI error: {e}")
        return jsonify({"error": f"AI service error: {str(e)}"}), 503

    except Exception as e:
        print(f"[Chat] Unexpected error: {traceback.format_exc()}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

    # ── Save to Database ─────────────────────────────
    saved_doc = MessageModel.save(
        username=username,
        message=message,
        reply=reply,
    )

    timestamp = saved_doc['timestamp'] if saved_doc else None

    # ── Return Response ──────────────────────────────
    return jsonify({
        "reply":     reply,
        "timestamp": timestamp,
        "saved":     saved_doc is not None,
    }), 200
