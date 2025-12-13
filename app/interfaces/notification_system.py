"""
Notification System Interface - Open/Closed Principle
Allows new notification types (e.g., Haptic Feedback) to be added without modification
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.models import NotificationType


class INotificationSystem(ABC):
    """
    Abstract interface for managing notifications.
    New notification types can be added by implementing this interface.
    """
    
    @abstractmethod
    def send_notification(
        self, 
        message: str, 
        notification_type: NotificationType,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Send a notification through the specified channel.
        
        Args:
            message: The notification message
            notification_type: Type of notification to send
            priority: Priority level (low, normal, high, critical)
            
        Returns:
            Dictionary with send status
        """
        pass
    
    @abstractmethod
    def send_visual_feedback(self, text: str, duration: int = 5) -> Dict[str, Any]:
        """
        Push visual text feedback for hearing-impaired users.
        
        Args:
            text: Text to display
            duration: Display duration in seconds
            
        Returns:
            Dictionary with status
        """
        pass
    
    @abstractmethod
    def get_notification_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's notification preferences.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with preferences
        """
        pass
    
    @abstractmethod
    def update_notification_preferences(
        self, 
        user_id: str, 
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user's notification preferences.
        
        Args:
            user_id: User identifier
            preferences: New preferences to set
            
        Returns:
            Dictionary with update status
        """
        pass
    
    @abstractmethod
    def get_supported_types(self) -> List[NotificationType]:
        """
        Get list of supported notification types.
        
        Returns:
            List of supported NotificationType enums
        """
        pass

