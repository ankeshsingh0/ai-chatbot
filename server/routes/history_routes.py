"""
NeuralChat — History Routes
─────────────────────────────
GET    /history  → Fetch chat history for a user
DELETE /clear    → Clear chat history for a user
"""

from flask import Blueprint, request, jsonify
from models.message_model import MessageModel
from config.settings import Config

# Blueprint for history routes
history_bp = Blueprint('history', __name__)


@history_bp.route('/history', methods=['GET'])
def get_history():
    """
    Retrieve paginated chat history for a user.

    Query Params:
        username (str):  Required. The user's display name.
        limit    (int):  Optional. Max records (default 50, max 200).

    Response (JSON):
        {
            "history": [...message objects...],
            "count":   int
        }
    """
    username = request.args.get('username', '').strip()

    if not username:
        return jsonify({"error": "username query parameter is required"}), 400

    # Clamp limit to prevent over-fetching
    try:
        limit = min(int(request.args.get('limit', 50)), 200)
    except (ValueError, TypeError):
        limit = 50

    history = MessageModel.get_history(username=username, limit=limit)

    return jsonify({
        "history": history,
        "count":   len(history),
    }), 200


@history_bp.route('/clear', methods=['DELETE'])
def clear_history():
    """
    Delete all chat history for a user.

    Request body (JSON):
        { "username": "display name" }

    Response (JSON):
        { "message": "...", "deleted_count": int }
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get('username', '').strip()

    if not username:
        return jsonify({"error": "username is required"}), 400

    deleted = MessageModel.clear_history(username=username)

    return jsonify({
        "message":       f"Cleared history for '{username}'",
        "deleted_count": deleted,
    }), 200
