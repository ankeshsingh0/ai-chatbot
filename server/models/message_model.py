"""
NeuralChat — Message Model
────────────────────────────
Handles all database operations for chat messages.
Schema:
  {
    username:   str,        # who sent the message
    message:    str,        # user's input
    reply:      str,        # AI's response
    timestamp:  datetime,   # when the exchange happened
    created_at: datetime    # document creation time
  }
"""

from datetime import datetime, timezone
from database.db import get_db


class MessageModel:
    """CRUD operations for chat message documents."""

    COLLECTION = 'messages'

    # ── CREATE ────────────────────────────────────────

    @staticmethod
    def save(username: str, message: str, reply: str) -> dict | None:
        """
        Save a user+bot exchange to the database.

        Args:
            username: The user's display name
            message:  The user's message
            reply:    The AI's reply

        Returns:
            The saved document dict, or None on failure
        """
        db = get_db()
        if db is None:
            return None

        now = datetime.now(timezone.utc)
        doc = {
            'username':   username,
            'message':    message,
            'reply':      reply,
            'timestamp':  now,
            'created_at': now,
        }

        try:
            result = db[MessageModel.COLLECTION].insert_one(doc)
            doc['_id'] = str(result.inserted_id)
            doc['timestamp'] = now.isoformat()
            return doc
        except Exception as e:
            print(f"[DB] Save error: {e}")
            return None

    # ── READ ──────────────────────────────────────────

    @staticmethod
    def get_history(username: str, limit: int = 50) -> list[dict]:
        """
        Retrieve chat history for a user, sorted oldest first.

        Args:
            username: The user's display name
            limit:    Max number of records to return

        Returns:
            List of message dicts
        """
        db = get_db()
        if db is None:
            return []

        try:
            cursor = (
                db[MessageModel.COLLECTION]
                .find({'username': username})
                .sort('timestamp', 1)   # ascending = oldest first
                .limit(limit)
            )

            results = []
            for doc in cursor:
                results.append({
                    'id':        str(doc['_id']),
                    'username':  doc.get('username', ''),
                    'message':   doc.get('message', ''),
                    'reply':     doc.get('reply', ''),
                    'timestamp': doc.get('timestamp', datetime.now(timezone.utc)).isoformat()
                    if hasattr(doc.get('timestamp'), 'isoformat')
                    else str(doc.get('timestamp', '')),
                })
            return results

        except Exception as e:
            print(f"[DB] History fetch error: {e}")
            return []

    @staticmethod
    def get_context(username: str, limit: int = 10) -> list[dict]:
        """
        Get recent messages for AI context (for conversation memory).
        Returns most recent N pairs.
        """
        db = get_db()
        if db is None:
            return []

        try:
            cursor = (
                db[MessageModel.COLLECTION]
                .find({'username': username})
                .sort('timestamp', -1)  # newest first
                .limit(limit)
            )
            # Reverse so oldest is first (correct for AI context)
            docs = list(cursor)
            docs.reverse()
            return [
                {'message': d.get('message', ''), 'reply': d.get('reply', '')}
                for d in docs
            ]
        except Exception as e:
            print(f"[DB] Context fetch error: {e}")
            return []

    # ── DELETE ────────────────────────────────────────

    @staticmethod
    def clear_history(username: str) -> int:
        """
        Delete all messages for a user.

        Returns:
            Number of documents deleted
        """
        db = get_db()
        if db is None:
            return 0

        try:
            result = db[MessageModel.COLLECTION].delete_many({'username': username})
            return result.deleted_count
        except Exception as e:
            print(f"[DB] Clear error: {e}")
            return 0
