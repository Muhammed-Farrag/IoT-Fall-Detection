"""
Flask Application Factory
Implements SOLID principles through modular design and dependency injection
"""
from flask import Flask, render_template
from config import Config


def create_app(config_class=Config):
    """
    Application factory pattern.
    Creates and configures the Flask application.
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints (Interface Segregation Principle)
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register index route
    register_index_route(app)
    
    return app


def register_blueprints(app):
    """
    Register all application blueprints.
    Demonstrates Interface Segregation - each dashboard has its own blueprint.
    """
    from app.blueprints import (
        primary_bp,
        caregiver_bp,
        health_professional_bp,
        emergency_bp
    )
    
    app.register_blueprint(primary_bp)
    app.register_blueprint(caregiver_bp)
    app.register_blueprint(health_professional_bp)
    app.register_blueprint(emergency_bp)
    
    print(" * Registered blueprints:")
    print("   - Primary User Dashboard: /primary")
    print("   - Caregiver Dashboard: /caregiver")
    print("   - Health Professional Dashboard: /health-professional")
    print("   - Emergency Service Dashboard: /emergency")


def register_error_handlers(app):
    """Register error handlers for common HTTP errors."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500


def register_index_route(app):
    """Register the index/landing page route."""
    
    @app.route('/')
    def index():
        """Landing page with links to all dashboards."""
        return render_template('index.html')

