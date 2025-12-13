"""
Blueprints package - Flask blueprints for modular routing
"""
from .primary_user import primary_bp
from .caregiver import caregiver_bp
from .health_professional import health_professional_bp
from .emergency import emergency_bp

__all__ = [
    'primary_bp',
    'caregiver_bp',
    'health_professional_bp',
    'emergency_bp'
]

