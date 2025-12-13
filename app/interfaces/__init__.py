"""
Interfaces package - Abstract Base Classes for dependency inversion
"""
from .input_handler import IInputHandler
from .notification_system import INotificationSystem
from .medical_knowledge_base import IMedicalKnowledgeBase
from .vision_service import IVisionService
from .settings_service import ISettingsService

__all__ = [
    'IInputHandler',
    'INotificationSystem',
    'IMedicalKnowledgeBase',
    'IVisionService',
    'ISettingsService'
]

