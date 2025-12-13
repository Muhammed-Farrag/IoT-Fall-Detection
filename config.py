"""
Application Configuration
Uses environment variables for sensitive data (12-factor app methodology)
"""
import os
from datetime import timedelta


class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Security Headers
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # JSON Configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Application Settings
    APP_NAME = 'NovaBot'
    APP_VERSION = '1.0.0'
    
    # Pagination
    ITEMS_PER_PAGE = 50
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    # CORS (if needed for API)
    CORS_ENABLED = os.environ.get('CORS_ENABLED', 'False').lower() == 'true'
    
    # Database (for future use)
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///novabot.db'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    ENV = 'development'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    ENV = 'production'
    
    # Production security settings
    SESSION_COOKIE_SECURE = True  # HTTPS only
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    ENV = 'testing'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

