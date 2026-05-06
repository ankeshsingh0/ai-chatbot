"""
NeuralChat — Flask Backend Server
──────────────────────────────────
Entry point. Creates the Flask app, registers blueprints,
and starts the development server.

Run:  python app.py
"""

import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config.settings import Config
from routes.chat_routes import chat_bp
from routes.history_routes import history_bp
from database.db import init_db


def create_app() -> Flask:
    """
    Application factory — creates and configures the Flask app.
    Returns a configured Flask instance.
    """
    app = Flask(__name__, static_folder='../client', static_url_path='')
    app.config.from_object(Config)

    # ── Allow cross-origin requests from the frontend ──
    # In production, replace "*" with your frontend domain.
    CORS(app, resources={r"/*": {"origins": "*"}})

    # ── Initialize MongoDB connection ──
    init_db(app)

    # ── Register route blueprints ──
    app.register_blueprint(chat_bp)
    app.register_blueprint(history_bp)

    # ── Serve frontend files ──
    @app.route('/')
    def serve_index():
        return send_from_directory('../client', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        if path and '.' in path:
            return send_from_directory('../client', path)
        return send_from_directory('../client', 'index.html')

    # ── Health check endpoint ──
    @app.route('/health')
    def health():
        return {"status": "ok", "service": "NeuralChat API"}, 200

    return app


# ── Run server ──
if __name__ == '__main__':
    app = create_app()
    print("🚀 NeuralChat server running on http://localhost:5000")
    app.run(
        host='0.0.0.0',
        port=int(Config.PORT),
        debug=Config.DEBUG,
    )
