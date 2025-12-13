"""
Emergency Service - Business logic for emergency response dashboard
Single Responsibility: Manages emergency-specific operations
"""
from typing import Dict, Any, List
from datetime import datetime


class EmergencyService:
    """
    Service for emergency response dashboard operations.
    Handles critical alerts and emergency response coordination.
    """
    
    def __init__(self):
        self._active_emergencies: Dict[str, Dict[str, Any]] = {}
    
    def get_emergency_details(self, emergency_id: str) -> Dict[str, Any]:
        """Get detailed information about an emergency event."""
        # Mock emergency data
        return {
            'success': True,
            'emergency': {
                'id': emergency_id,
                'type': 'FALL_DETECTED',
                'severity': 'CRITICAL',
                'status': 'ACTIVE',
                'patient': {
                    'id': 'patient_001',
                    'name': 'John Doe',
                    'age': 72,
                    'medical_conditions': ['Osteoporosis', 'Hypertension'],
                    'allergies': ['Penicillin'],
                    'emergency_contacts': [
                        {'name': 'Jane Doe', 'relation': 'Daughter', 'phone': '+1-555-0101'}
                    ]
                },
                'location': {
                    'latitude': 40.7128,
                    'longitude': -74.0060,
                    'address': '123 Main Street, New York, NY 10001',
                    'unit': 'Apt 4B',
                    'accuracy': 3.5  # meters
                },
                'timestamp': datetime.utcnow().isoformat(),
                'detected_by': 'Fall Detection Sensor',
                'vitals_at_incident': {
                    'heart_rate': 95,
                    'blood_pressure': '140/90',
                    'oxygen_saturation': 94
                },
                'response_time_elapsed': '00:02:34',
                'nearest_responders': [
                    {'unit': 'EMS-12', 'distance': '1.2 km', 'eta': '4 minutes'},
                    {'unit': 'EMS-08', 'distance': '2.1 km', 'eta': '6 minutes'}
                ]
            }
        }
    
    def get_critical_data(self, emergency_id: str) -> Dict[str, Any]:
        """Get critical data for first responders."""
        return {
            'success': True,
            'critical_data': {
                'event_nature': 'FALL DETECTED',
                'time_elapsed': '00:02:45',
                'location': {
                    'coordinates': '40.7128, -74.0060',
                    'address': '123 Main Street, New York, NY 10001',
                    'floor': '4th Floor',
                    'access_notes': 'Doorman on duty 24/7, elevator access'
                },
                'patient_summary': {
                    'age': 72,
                    'gender': 'Male',
                    'mobility': 'Requires walker',
                    'cognitive_status': 'Alert and oriented',
                    'living_situation': 'Lives alone'
                },
                'immediate_concerns': [
                    'Possible hip fracture',
                    'Patient has osteoporosis',
                    'History of falls',
                    'Allergic to Penicillin'
                ],
                'medications': [
                    'Alendronate (Osteoporosis)',
                    'Lisinopril (Blood Pressure)',
                    'Aspirin (Blood thinner)'
                ],
                'dnr_status': False,
                'healthcare_proxy': {
                    'name': 'Jane Doe',
                    'phone': '+1-555-0101',
                    'contacted': True,
                    'eta': '15 minutes'
                }
            }
        }
    
    def update_response_status(
        self, 
        emergency_id: str,
        status: str,
        responder_id: str,
        notes: str = None
    ) -> Dict[str, Any]:
        """Update emergency response status."""
        valid_statuses = ['DISPATCHED', 'EN_ROUTE', 'ON_SCENE', 'RESOLVED', 'CANCELLED']
        
        if status not in valid_statuses:
            return {
                'success': False,
                'message': f'Invalid status. Must be one of: {valid_statuses}'
            }
        
        update = {
            'emergency_id': emergency_id,
            'status': status,
            'responder_id': responder_id,
            'timestamp': datetime.utcnow().isoformat(),
            'notes': notes
        }
        
        return {
            'success': True,
            'message': f'Emergency status updated to {status}',
            'update': update
        }
    
    def get_environmental_data(self, emergency_id: str) -> Dict[str, Any]:
        """Get environmental data from the scene."""
        return {
            'success': True,
            'environmental_data': {
                'smoke_detected': False,
                'temperature': 22.0,  # Celsius
                'carbon_monoxide': 0,  # ppm
                'air_quality': 'Good',
                'lighting': 'Adequate',
                'audio_detected': 'Distress call detected',
                'movement_detected': 'Limited movement in last 2 minutes',
                'doors_locked': True,
                'windows_status': 'Closed'
            }
        }
    
    def get_live_audio_stream(self, emergency_id: str) -> Dict[str, Any]:
        """Get live audio stream from the device."""
        return {
            'success': True,
            'audio_stream': {
                'stream_url': f'/stream/audio/{emergency_id}',
                'protocol': 'webrtc',
                'codec': 'opus',
                'two_way_enabled': True,
                'status': 'active'
            }
        }
    
    def send_reassurance_message(
        self, 
        emergency_id: str,
        message: str
    ) -> Dict[str, Any]:
        """Send a reassurance message to the patient."""
        return {
            'success': True,
            'message': 'Reassurance message sent',
            'delivery': {
                'method': 'audio',
                'text': message,
                'timestamp': datetime.utcnow().isoformat(),
                'delivered': True
            }
        }
    
    def get_nearby_facilities(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get nearby medical facilities."""
        return {
            'success': True,
            'facilities': [
                {
                    'name': 'New York General Hospital',
                    'type': 'Emergency Room',
                    'distance': 2.3,  # km
                    'eta': '5 minutes',
                    'trauma_level': 'Level I',
                    'current_wait': '15 minutes',
                    'beds_available': 3
                },
                {
                    'name': 'Downtown Medical Center',
                    'type': 'Urgent Care',
                    'distance': 1.1,
                    'eta': '3 minutes',
                    'trauma_level': 'N/A',
                    'current_wait': '5 minutes',
                    'beds_available': 5
                }
            ]
        }
    
    def log_incident_report(
        self, 
        emergency_id: str,
        report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Log incident report for records."""
        report = {
            'id': f"incident_{datetime.utcnow().timestamp()}",
            'emergency_id': emergency_id,
            'report_data': report_data,
            'timestamp': datetime.utcnow().isoformat(),
            'filed_by': report_data.get('responder_id', 'system')
        }
        
        return {
            'success': True,
            'message': 'Incident report logged',
            'report': report
        }

