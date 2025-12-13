"""
Caregiver Service - Business logic for caregiver dashboard
Single Responsibility: Manages caregiver-specific operations
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


class CaregiverService:
    """
    Service for caregiver dashboard operations.
    Handles monitoring, alerts, and patient status.
    """
    
    def __init__(self):
        self._alerts: List[Dict[str, Any]] = []
        self._device_status: Dict[str, Any] = {
            'battery_level': 85,
            'last_sync': datetime.utcnow().isoformat(),
            'connection_status': 'connected',
            'firmware_version': '2.1.0'
        }
    
    def get_patient_status(self, patient_id: str) -> Dict[str, Any]:
        """Get current patient status and vital information."""
        return {
            'success': True,
            'patient_id': patient_id,
            'status': {
                'current_activity': 'resting',
                'location': 'Home - Living Room',
                'last_movement': '5 minutes ago',
                'alerts_today': len([a for a in self._alerts if self._is_today(a['timestamp'])]),
                'device_status': self._device_status,
                'wellbeing_score': 8.5
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_live_video_stream_url(self, patient_id: str) -> Dict[str, Any]:
        """Get URL for live video stream."""
        # In a real implementation, this would connect to actual video streaming service
        return {
            'success': True,
            'stream_url': f'/stream/video/{patient_id}',
            'stream_type': 'webrtc',
            'resolution': '1280x720',
            'framerate': 30
        }
    
    def get_location(self, patient_id: str) -> Dict[str, Any]:
        """Get patient's current GPS location."""
        # Mock GPS coordinates
        return {
            'success': True,
            'patient_id': patient_id,
            'location': {
                'latitude': 40.7128,
                'longitude': -74.0060,
                'address': '123 Main Street, New York, NY 10001',
                'accuracy': 5.2,  # meters
                'last_updated': datetime.utcnow().isoformat()
            }
        }
    
    def get_alerts(
        self, 
        patient_id: str, 
        limit: int = 50,
        severity: str = None
    ) -> Dict[str, Any]:
        """Get alert history for a patient."""
        # Generate mock alerts if none exist
        if not self._alerts:
            self._generate_mock_alerts(patient_id)
        
        alerts = self._alerts
        
        if severity:
            alerts = [a for a in alerts if a['severity'] == severity]
        
        alerts = alerts[:limit]
        
        return {
            'success': True,
            'alerts': alerts,
            'total': len(alerts),
            'unread': len([a for a in alerts if not a.get('read', False)])
        }
    
    def mark_alert_read(self, alert_id: str) -> Dict[str, Any]:
        """Mark an alert as read."""
        for alert in self._alerts:
            if alert['id'] == alert_id:
                alert['read'] = True
                alert['read_at'] = datetime.utcnow().isoformat()
                return {
                    'success': True,
                    'message': 'Alert marked as read'
                }
        
        return {
            'success': False,
            'message': 'Alert not found'
        }
    
    def get_device_battery(self, patient_id: str) -> Dict[str, Any]:
        """Get device battery status."""
        return {
            'success': True,
            'battery': {
                'level': self._device_status['battery_level'],
                'charging': False,
                'estimated_hours_remaining': 8.5,
                'health': 'good'
            }
        }
    
    def update_care_notes(
        self, 
        patient_id: str,
        note: str,
        caregiver_id: str
    ) -> Dict[str, Any]:
        """Add a care note for the patient."""
        note_entry = {
            'id': f"note_{datetime.utcnow().timestamp()}",
            'patient_id': patient_id,
            'caregiver_id': caregiver_id,
            'note': note,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return {
            'success': True,
            'message': 'Care note added',
            'note': note_entry
        }
    
    def _generate_mock_alerts(self, patient_id: str):
        """Generate mock alerts for demonstration."""
        alert_types = [
            ('Fall Detected', 'critical'),
            ('Medication Missed', 'high'),
            ('Low Battery', 'medium'),
            ('Left Safe Zone', 'high'),
            ('Unusual Inactivity', 'medium')
        ]
        
        for i in range(10):
            alert_type, severity = random.choice(alert_types)
            timestamp = datetime.utcnow() - timedelta(hours=i*2)
            
            self._alerts.append({
                'id': f"alert_{timestamp.timestamp()}",
                'patient_id': patient_id,
                'type': alert_type,
                'severity': severity,
                'message': f'{alert_type} detected',
                'timestamp': timestamp.isoformat(),
                'read': i > 3,
                'location': 'Home'
            })
    
    def _is_today(self, timestamp_str: str) -> bool:
        """Check if timestamp is today."""
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            return timestamp.date() == datetime.utcnow().date()
        except:
            return False

