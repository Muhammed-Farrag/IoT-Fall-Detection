"""
Communication Service - Implements IInputHandler and INotificationSystem
Single Responsibility: Handles all communication-related business logic
"""
from typing import Dict, Any, List
from datetime import datetime
from app.interfaces import IInputHandler, INotificationSystem
from app.models import InputMode, NotificationType


class CommunicationService(IInputHandler, INotificationSystem):
    """
    Concrete implementation of communication services.
    Demonstrates Single Responsibility: Only handles communication logic.
    """
    
    def __init__(self):
        self._active_mode: InputMode = InputMode.TOUCH
        self._mode_status: Dict[InputMode, bool] = {
            InputMode.SPOKEN: True,
            InputMode.SIGN_LANGUAGE: True,
            InputMode.TOUCH: True
        }
        self._notification_preferences: Dict[str, Any] = {}
        self._visual_feedback_queue: List[Dict[str, Any]] = []
    
    # IInputHandler implementation
    
    def set_active_mode(self, mode: InputMode) -> Dict[str, Any]:
        """Set the active input mode."""
        if not self.validate_mode_availability(mode):
            return {
                'success': False,
                'message': f'Input mode {mode.value} is not available',
                'active_mode': self._active_mode.value
            }
        
        self._active_mode = mode
        return {
            'success': True,
            'message': f'Input mode changed to {mode.value}',
            'active_mode': mode.value,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_active_mode(self) -> InputMode:
        """Get the currently active input mode."""
        return self._active_mode
    
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input based on the active mode."""
        mode = self._active_mode
        
        processors = {
            InputMode.SPOKEN: self._process_spoken_input,
            InputMode.SIGN_LANGUAGE: self._process_sign_language_input,
            InputMode.TOUCH: self._process_touch_input
        }
        
        processor = processors.get(mode)
        if processor:
            return processor(input_data)
        
        return {
            'success': False,
            'message': 'Unknown input mode'
        }
    
    def validate_mode_availability(self, mode: InputMode) -> bool:
        """Check if a specific input mode is available."""
        return self._mode_status.get(mode, False)
    
    # INotificationSystem implementation
    
    def send_notification(
        self, 
        message: str, 
        notification_type: NotificationType,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Send a notification through the specified channel."""
        notification = {
            'id': self._generate_notification_id(),
            'message': message,
            'type': notification_type.value,
            'priority': priority,
            'timestamp': datetime.utcnow().isoformat(),
            'delivered': True
        }
        
        # In a real implementation, this would interface with actual notification systems
        return {
            'success': True,
            'notification': notification,
            'message': f'Notification sent via {notification_type.value}'
        }
    
    def send_visual_feedback(self, text: str, duration: int = 5) -> Dict[str, Any]:
        """Push visual text feedback for hearing-impaired users."""
        feedback = {
            'id': self._generate_notification_id(),
            'text': text,
            'duration': duration,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'visual_feedback'
        }
        
        self._visual_feedback_queue.append(feedback)
        
        return {
            'success': True,
            'feedback': feedback,
            'queue_size': len(self._visual_feedback_queue)
        }
    
    def get_notification_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user's notification preferences."""
        return self._notification_preferences.get(user_id, {
            'visual': True,
            'audio': True,
            'haptic': False,
            'priority_filter': 'normal'
        })
    
    def update_notification_preferences(
        self, 
        user_id: str, 
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update user's notification preferences."""
        self._notification_preferences[user_id] = preferences
        
        return {
            'success': True,
            'message': 'Notification preferences updated',
            'preferences': preferences
        }
    
    def get_supported_types(self) -> List[NotificationType]:
        """Get list of supported notification types."""
        return [
            NotificationType.VISUAL,
            NotificationType.AUDIO,
            NotificationType.HAPTIC
        ]
    
    def get_visual_feedback_queue(self) -> List[Dict[str, Any]]:
        """Get the current visual feedback queue."""
        return self._visual_feedback_queue
    
    def clear_visual_feedback(self, feedback_id: str) -> Dict[str, Any]:
        """Clear a specific visual feedback from the queue."""
        self._visual_feedback_queue = [
            fb for fb in self._visual_feedback_queue 
            if fb['id'] != feedback_id
        ]
        
        return {
            'success': True,
            'message': 'Visual feedback cleared',
            'queue_size': len(self._visual_feedback_queue)
        }
    
    # Private helper methods
    
    def _process_spoken_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process spoken input (speech-to-text)."""
        audio_data = input_data.get('audio', '')
        
        # In a real implementation, this would use a speech-to-text API
        transcribed_text = input_data.get('text', '[Transcribed speech]')
        
        return {
            'success': True,
            'mode': InputMode.SPOKEN.value,
            'input_type': 'spoken',
            'transcribed_text': transcribed_text,
            'confidence': 0.95,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _process_sign_language_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process sign language input (computer vision)."""
        video_frame = input_data.get('frame', '')
        
        # In a real implementation, this would use a sign language recognition API
        interpreted_text = input_data.get('text', '[Interpreted sign language]')
        
        return {
            'success': True,
            'mode': InputMode.SIGN_LANGUAGE.value,
            'input_type': 'sign_language',
            'interpreted_text': interpreted_text,
            'confidence': 0.88,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _process_touch_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process touch input."""
        touch_data = input_data.get('touch', {})
        
        return {
            'success': True,
            'mode': InputMode.TOUCH.value,
            'input_type': 'touch',
            'action': touch_data.get('action', 'tap'),
            'coordinates': touch_data.get('coordinates', {'x': 0, 'y': 0}),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _generate_notification_id(self) -> str:
        """Generate a unique notification ID."""
        return f"notif_{datetime.utcnow().timestamp()}"

