"""
NeuralChat — Database Module
──────────────────────────────
Manages MongoDB connection using PyMongo.
Provides a global `db` object used by models.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from flask import Flask
import sys


# Global database reference — populated by init_db()
db = None
client = None


def init_db(app: Flask) -> None:
    """
    Initialize MongoDB connection using app config.
    Called once at app startup.
    """
    global db, client

    mongo_uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/')
    db_name   = app.config.get('DB_NAME',   'neuralchat')

    try:
        # serverSelectionTimeoutMS: fail fast if MongoDB not available
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

        # Ping to confirm connection
        client.admin.command('ping')
        db = client[db_name]

        print(f"✅ MongoDB connected → '{db_name}' database")

        # Ensure indexes for performance
        _create_indexes()

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("   Running without database — chat history will not persist.")
        db = None

    except Exception as e:
        print(f"❌ Unexpected database error: {e}")
        db = None


def _create_indexes() -> None:
    """Create database indexes for query performance."""
    if db is None:
        return
    try:
        # Index on username for fast history lookups
        db.messages.create_index('username')
        # Compound index for sorted history per user
        db.messages.create_index([('username', 1), ('timestamp', -1)])
    except Exception as e:
        print(f"⚠️  Index creation warning: {e}")


def get_db():
    """Return the active database instance."""
    return db


def is_connected() -> bool:
    """Return True if MongoDB is connected."""
    return db is not None
