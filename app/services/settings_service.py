"""
Settings Service - Implements ISettingsService
Single Responsibility: Handles all user settings and preferences
"""
from typing import Dict, Any
from datetime import datetime
from app.interfaces import ISettingsService
from app.models import DataSharingLevel, AccessibilityMode


class SettingsService(ISettingsService):
    """
    Concrete implementation of settings management.
    Demonstrates Single Responsibility: Only manages user preferences.
    """
    
    def __init__(self):
        self._privacy_settings: Dict[str, Dict[str, Any]] = {}
        self._accessibility_settings: Dict[str, Dict[str, Any]] = {}
    
    def get_privacy_settings(self, user_id: str) -> Dict[str, Any]:
        """Get user's privacy settings."""
        return self._privacy_settings.get(user_id, {
            'data_sharing': DataSharingLevel.STANDARD.value,
            'location_tracking': True,
            'health_data_sharing': False,
            'anonymize_data': True,
            'third_party_sharing': False,
            'data_retention_days': 90
        })
    
    def update_data_sharing(
        self, 
        user_id: str, 
        sharing_level: DataSharingLevel
    ) -> Dict[str, Any]:
        """Update data sharing preferences."""
        if user_id not in self._privacy_settings:
            self._privacy_settings[user_id] = self.get_privacy_settings(user_id)
        
        self._privacy_settings[user_id]['data_sharing'] = sharing_level.value
        self._privacy_settings[user_id]['updated_at'] = datetime.utcnow().isoformat()
        
        # Adjust related settings based on sharing level
        if sharing_level == DataSharingLevel.NONE:
            self._privacy_settings[user_id]['location_tracking'] = False
            self._privacy_settings[user_id]['health_data_sharing'] = False
            self._privacy_settings[user_id]['third_party_sharing'] = False
        
        return {
            'success': True,
            'message': f'Data sharing updated to {sharing_level.value}',
            'settings': self._privacy_settings[user_id]
        }
    
    def get_accessibility_settings(self, user_id: str) -> Dict[str, Any]:
        """Get user's accessibility settings."""
        return self._accessibility_settings.get(user_id, {
            'mode': AccessibilityMode.MULTIMODAL.value,
            'text_only': False,
            'voice_enabled': True,
            'sign_language_enabled': True,
            'haptic_feedback': True,
            'high_contrast': True,
            'font_size': 'large',
            'screen_reader': False,
            'audio_descriptions': True
        })
    
    def update_accessibility_mode(
        self, 
        user_id: str, 
        mode: AccessibilityMode
    ) -> Dict[str, Any]:
        """Update accessibility preferences."""
        if user_id not in self._accessibility_settings:
            self._accessibility_settings[user_id] = self.get_accessibility_settings(user_id)
        
        self._accessibility_settings[user_id]['mode'] = mode.value
        self._accessibility_settings[user_id]['updated_at'] = datetime.utcnow().isoformat()
        
        # Adjust related settings based on mode
        if mode == AccessibilityMode.TEXT_ONLY:
            self._accessibility_settings[user_id]['text_only'] = True
            self._accessibility_settings[user_id]['voice_enabled'] = False
            self._accessibility_settings[user_id]['audio_descriptions'] = False
        elif mode == AccessibilityMode.VOICE_ENABLED:
            self._accessibility_settings[user_id]['text_only'] = False
            self._accessibility_settings[user_id]['voice_enabled'] = True
            self._accessibility_settings[user_id]['audio_descriptions'] = True
        elif mode == AccessibilityMode.MULTIMODAL:
            self._accessibility_settings[user_id]['text_only'] = False
            self._accessibility_settings[user_id]['voice_enabled'] = True
            self._accessibility_settings[user_id]['sign_language_enabled'] = True
        
        return {
            'success': True,
            'message': f'Accessibility mode updated to {mode.value}',
            'settings': self._accessibility_settings[user_id]
        }
    
    def toggle_communication_preference(
        self, 
        user_id: str, 
        preference: str, 
        enabled: bool
    ) -> Dict[str, Any]:
        """Toggle specific communication preferences."""
        if user_id not in self._accessibility_settings:
            self._accessibility_settings[user_id] = self.get_accessibility_settings(user_id)
        
        valid_preferences = [
            'text_only', 'voice_enabled', 'sign_language_enabled',
            'haptic_feedback', 'audio_descriptions'
        ]
        
        if preference not in valid_preferences:
            return {
                'success': False,
                'message': f'Invalid preference: {preference}'
            }
        
        self._accessibility_settings[user_id][preference] = enabled
        self._accessibility_settings[user_id]['updated_at'] = datetime.utcnow().isoformat()
        
        return {
            'success': True,
            'message': f'{preference} {"enabled" if enabled else "disabled"}',
            'preference': preference,
            'enabled': enabled
        }
    
    def get_all_settings(self, user_id: str) -> Dict[str, Any]:
        """Get all settings for a user."""
        return {
            'success': True,
            'privacy': self.get_privacy_settings(user_id),
            'accessibility': self.get_accessibility_settings(user_id),
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def reset_to_defaults(self, user_id: str) -> Dict[str, Any]:
        """Reset all settings to defaults."""
        if user_id in self._privacy_settings:
            del self._privacy_settings[user_id]
        if user_id in self._accessibility_settings:
            del self._accessibility_settings[user_id]
        
        return {
            'success': True,
            'message': 'Settings reset to defaults',
            'settings': self.get_all_settings(user_id)
        }

