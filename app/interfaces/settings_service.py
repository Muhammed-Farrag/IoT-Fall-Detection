"""
Settings Service Interface - Single Responsibility & Dependency Inversion
Manages user preferences, privacy, and accessibility settings
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models import DataSharingLevel, AccessibilityMode


class ISettingsService(ABC):
    """
    Abstract interface for managing user settings.
    Separates settings management from business logic.
    """
    
    @abstractmethod
    def get_privacy_settings(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's privacy settings.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with privacy settings
        """
        pass
    
    @abstractmethod
    def update_data_sharing(
        self, 
        user_id: str, 
        sharing_level: DataSharingLevel
    ) -> Dict[str, Any]:
        """
        Update data sharing preferences.
        
        Args:
            user_id: User identifier
            sharing_level: Desired data sharing level
            
        Returns:
            Dictionary with update status
        """
        pass
    
    @abstractmethod
    def get_accessibility_settings(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's accessibility settings.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with accessibility settings
        """
        pass
    
    @abstractmethod
    def update_accessibility_mode(
        self, 
        user_id: str, 
        mode: AccessibilityMode
    ) -> Dict[str, Any]:
        """
        Update accessibility preferences.
        
        Args:
            user_id: User identifier
            mode: Desired accessibility mode
            
        Returns:
            Dictionary with update status
        """
        pass
    
    @abstractmethod
    def toggle_communication_preference(
        self, 
        user_id: str, 
        preference: str, 
        enabled: bool
    ) -> Dict[str, Any]:
        """
        Toggle specific communication preferences.
        
        Args:
            user_id: User identifier
            preference: Preference name (e.g., 'text_only', 'voice_enabled')
            enabled: Whether to enable or disable
            
        Returns:
            Dictionary with update status
        """
        pass
    
    @abstractmethod
    def get_all_settings(self, user_id: str) -> Dict[str, Any]:
        """
        Get all settings for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with all user settings
        """
        pass

