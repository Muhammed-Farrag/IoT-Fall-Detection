"""
NovaCare Fall Detection System - App Package
"""
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()
socketio = SocketIO()


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config_class)
    
    # Ensure recordings folder exists
    os.makedirs(app.config['RECORDINGS_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')
    
    # Create database tables
    with app.app_context():
        from app.models.database import Alert
        db.create_all()
    
    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register socket events
    from app.sockets import events
    
    return app
