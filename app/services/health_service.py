"""
Health Service - Implements IMedicalKnowledgeBase
Single Responsibility: Handles all health and medication-related business logic
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.interfaces import IMedicalKnowledgeBase, INotificationSystem
from app.models import NotificationType


class HealthService(IMedicalKnowledgeBase):
    """
    Concrete implementation of health services.
    Demonstrates Dependency Injection: Takes INotificationSystem as dependency.
    """
    
    def __init__(self, notification_service: INotificationSystem):
        self._notification_service = notification_service
        self._medication_schedules: Dict[str, List[Dict[str, Any]]] = {}
        self._query_history: Dict[str, Dict[str, Any]] = {}
        self._medical_disclaimer = (
            "⚠️ This information is for educational purposes only. "
            "Always consult with a qualified healthcare professional "
            "before making any medical decisions."
        )
    
    # Medication Management Methods
    
    def create_schedule(
        self, 
        user_id: str, 
        medication_name: str,
        dosage: str,
        frequency: str,
        times: List[str],
        start_date: str
    ) -> Dict[str, Any]:
        """Create a new medication schedule."""
        schedule = {
            'id': self._generate_schedule_id(),
            'medication_name': medication_name,
            'dosage': dosage,
            'frequency': frequency,
            'times': times,
            'start_date': start_date,
            'active': True,
            'created_at': datetime.utcnow().isoformat()
        }
        
        if user_id not in self._medication_schedules:
            self._medication_schedules[user_id] = []
        
        self._medication_schedules[user_id].append(schedule)
        
        return {
            'success': True,
            'message': 'Medication schedule created',
            'schedule': schedule
        }
    
    def update_schedule(
        self, 
        user_id: str, 
        schedule_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing medication schedule."""
        user_schedules = self._medication_schedules.get(user_id, [])
        
        for schedule in user_schedules:
            if schedule['id'] == schedule_id:
                schedule.update(updates)
                schedule['updated_at'] = datetime.utcnow().isoformat()
                
                return {
                    'success': True,
                    'message': 'Medication schedule updated',
                    'schedule': schedule
                }
        
        return {
            'success': False,
            'message': 'Schedule not found'
        }
    
    def get_schedules(self, user_id: str) -> Dict[str, Any]:
        """Get all medication schedules for a user."""
        schedules = self._medication_schedules.get(user_id, [])
        active_schedules = [s for s in schedules if s.get('active', False)]
        
        return {
            'success': True,
            'schedules': active_schedules,
            'total': len(active_schedules)
        }
    
    def get_next_medication(self, user_id: str) -> Dict[str, Any]:
        """Get the next scheduled medication."""
        schedules = self._medication_schedules.get(user_id, [])
        
        if not schedules:
            return {
                'success': True,
                'next_medication': None,
                'message': 'No medications scheduled'
            }
        
        # In a real implementation, this would calculate the actual next time
        next_med = schedules[0] if schedules else None
        
        return {
            'success': True,
            'next_medication': {
                'name': next_med['medication_name'],
                'dosage': next_med['dosage'],
                'scheduled_time': next_med['times'][0] if next_med['times'] else 'N/A',
                'time_until': '2 hours 30 minutes'
            }
        }
    
    def send_medication_alert(
        self, 
        user_id: str,
        medication_name: str,
        alert_type: str = "visual"
    ) -> Dict[str, Any]:
        """Send a medication reminder alert."""
        message = f"Time to take {medication_name}"
        
        notification_type_map = {
            'visual': NotificationType.VISUAL,
            'audio': NotificationType.AUDIO,
            'both': NotificationType.VISUAL  # Would send both in real implementation
        }
        
        notification_type = notification_type_map.get(alert_type, NotificationType.VISUAL)
        
        result = self._notification_service.send_notification(
            message=message,
            notification_type=notification_type,
            priority='high'
        )
        
        return {
            'success': True,
            'message': 'Medication alert sent',
            'alert_details': result
        }
    
    # IMedicalKnowledgeBase implementation (RAG System)
    
    def query(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Query the medical knowledge base using RAG."""
        query_id = self._generate_query_id()
        
        # In a real implementation, this would:
        # 1. Embed the question using a language model
        # 2. Search a vector database of medical documents
        # 3. Generate a response using RAG
        # 4. Verify the response for medical accuracy
        
        response_text = self._generate_mock_response(question)
        
        response = {
            'query_id': query_id,
            'question': question,
            'answer': response_text,
            'sources': self._get_mock_sources(),
            'confidence': 0.92,
            'timestamp': datetime.utcnow().isoformat(),
            'verified': True
        }
        
        # Add disclaimer
        response = self.add_disclaimer(response)
        
        # Store in history
        self._query_history[query_id] = response
        
        return {
            'success': True,
            'response': response
        }
    
    def verify_response(self, response: str) -> Dict[str, Any]:
        """Verify the medical accuracy of a response."""
        # In a real implementation, this would use medical fact-checking
        return {
            'verified': True,
            'reliability_score': 0.91,
            'verification_method': 'medical_knowledge_base',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_sources(self, query_id: str) -> List[Dict[str, Any]]:
        """Get source documents used for a specific query."""
        query = self._query_history.get(query_id, {})
        return query.get('sources', [])
    
    def add_disclaimer(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Add medical disclaimer to the response."""
        response['disclaimer'] = self._medical_disclaimer
        return response
    
    # Private helper methods
    
    def _generate_schedule_id(self) -> str:
        """Generate a unique schedule ID."""
        return f"sched_{datetime.utcnow().timestamp()}"
    
    def _generate_query_id(self) -> str:
        """Generate a unique query ID."""
        return f"query_{datetime.utcnow().timestamp()}"
    
    def _generate_mock_response(self, question: str) -> str:
        """Generate a mock RAG response for demonstration."""
        return (
            f"Based on current medical knowledge regarding '{question}', "
            "here is what the research indicates: [RAG-generated response would appear here]. "
            "This information is derived from peer-reviewed medical sources."
        )
    
    def _get_mock_sources(self) -> List[Dict[str, Any]]:
        """Get mock source citations."""
        return [
            {
                'title': 'Medical Journal Article',
                'citation': 'Journal of Medicine, 2024',
                'relevance': 0.95
            },
            {
                'title': 'Clinical Guidelines',
                'citation': 'WHO Guidelines, 2023',
                'relevance': 0.88
            }
        ]

