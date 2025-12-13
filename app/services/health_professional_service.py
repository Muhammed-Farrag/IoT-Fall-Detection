"""
Health Professional Service - Business logic for health professional dashboard
Single Responsibility: Manages health professional-specific operations
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


class HealthProfessionalService:
    """
    Service for health professional dashboard operations.
    Handles patient vitals, reports, and medical data.
    """
    
    def __init__(self):
        self._vitals_history: Dict[str, List[Dict[str, Any]]] = {}
    
    def get_current_vitals(self, patient_id: str) -> Dict[str, Any]:
        """Get current vital signs for a patient."""
        return {
            'success': True,
            'patient_id': patient_id,
            'vitals': {
                'heart_rate': {
                    'value': 72,
                    'unit': 'bpm',
                    'status': 'normal',
                    'timestamp': datetime.utcnow().isoformat()
                },
                'blood_pressure': {
                    'systolic': 120,
                    'diastolic': 80,
                    'unit': 'mmHg',
                    'status': 'normal',
                    'timestamp': datetime.utcnow().isoformat()
                },
                'oxygen_saturation': {
                    'value': 98,
                    'unit': '%',
                    'status': 'normal',
                    'timestamp': datetime.utcnow().isoformat()
                },
                'temperature': {
                    'value': 36.8,
                    'unit': '°C',
                    'status': 'normal',
                    'timestamp': datetime.utcnow().isoformat()
                },
                'respiratory_rate': {
                    'value': 16,
                    'unit': 'breaths/min',
                    'status': 'normal',
                    'timestamp': datetime.utcnow().isoformat()
                }
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_vitals_history(
        self, 
        patient_id: str,
        vital_type: str = None,
        hours: int = 24
    ) -> Dict[str, Any]:
        """Get historical vital signs data."""
        # Generate mock historical data
        history = self._generate_vitals_history(patient_id, vital_type, hours)
        
        return {
            'success': True,
            'patient_id': patient_id,
            'vital_type': vital_type or 'all',
            'time_range': f'{hours} hours',
            'data': history
        }
    
    def get_health_trends(self, patient_id: str) -> Dict[str, Any]:
        """Get health trends and analytics."""
        return {
            'success': True,
            'patient_id': patient_id,
            'trends': {
                'heart_rate': {
                    'average': 74,
                    'trend': 'stable',
                    'change_percent': 0.5
                },
                'blood_pressure': {
                    'average_systolic': 122,
                    'average_diastolic': 82,
                    'trend': 'improving',
                    'change_percent': -2.1
                },
                'oxygen_saturation': {
                    'average': 97,
                    'trend': 'stable',
                    'change_percent': 0.0
                },
                'activity_level': {
                    'average_steps': 5200,
                    'trend': 'increasing',
                    'change_percent': 8.3
                }
            },
            'period': '7 days',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def generate_health_report(
        self, 
        patient_id: str,
        report_type: str = 'comprehensive'
    ) -> Dict[str, Any]:
        """Generate a health report PDF."""
        report_id = f"report_{datetime.utcnow().timestamp()}"
        
        return {
            'success': True,
            'report': {
                'id': report_id,
                'patient_id': patient_id,
                'type': report_type,
                'format': 'pdf',
                'download_url': f'/api/health-professional/reports/{report_id}/download',
                'generated_at': datetime.utcnow().isoformat(),
                'includes': [
                    'Vital Signs Summary',
                    'Medication Adherence',
                    'Activity Levels',
                    'Alert History',
                    'Health Trends'
                ]
            }
        }
    
    def get_medication_adherence(self, patient_id: str) -> Dict[str, Any]:
        """Get medication adherence statistics."""
        return {
            'success': True,
            'patient_id': patient_id,
            'adherence': {
                'overall_rate': 92.5,
                'missed_doses_week': 2,
                'on_time_rate': 88.0,
                'medications': [
                    {
                        'name': 'Medication A',
                        'adherence_rate': 95.0,
                        'doses_taken': 19,
                        'doses_scheduled': 20
                    },
                    {
                        'name': 'Medication B',
                        'adherence_rate': 90.0,
                        'doses_taken': 9,
                        'doses_scheduled': 10
                    }
                ]
            },
            'period': '7 days',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_fall_incidents(self, patient_id: str, days: int = 30) -> Dict[str, Any]:
        """Get fall incident history."""
        # Generate mock fall incidents
        incidents = []
        for i in range(3):
            incident_time = datetime.utcnow() - timedelta(days=i*7)
            incidents.append({
                'id': f"fall_{incident_time.timestamp()}",
                'timestamp': incident_time.isoformat(),
                'severity': random.choice(['minor', 'moderate']),
                'location': random.choice(['Living Room', 'Bathroom', 'Bedroom']),
                'response_time': f'{random.randint(1, 5)} minutes',
                'injuries': random.choice([False, False, True]),
                'medical_attention': False
            })
        
        return {
            'success': True,
            'patient_id': patient_id,
            'incidents': incidents,
            'total_incidents': len(incidents),
            'period': f'{days} days'
        }
    
    def add_clinical_note(
        self, 
        patient_id: str,
        note: str,
        professional_id: str
    ) -> Dict[str, Any]:
        """Add a clinical note for the patient."""
        note_entry = {
            'id': f"clinical_{datetime.utcnow().timestamp()}",
            'patient_id': patient_id,
            'professional_id': professional_id,
            'note': note,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'clinical_observation'
        }
        
        return {
            'success': True,
            'message': 'Clinical note added',
            'note': note_entry
        }
    
    def _generate_vitals_history(
        self, 
        patient_id: str,
        vital_type: str,
        hours: int
    ) -> List[Dict[str, Any]]:
        """Generate mock vitals history data."""
        history = []
        data_points = hours  # One per hour
        
        for i in range(data_points):
            timestamp = datetime.utcnow() - timedelta(hours=i)
            
            history.append({
                'timestamp': timestamp.isoformat(),
                'heart_rate': 70 + random.randint(-5, 5),
                'oxygen_saturation': 97 + random.randint(-1, 2),
                'systolic_bp': 120 + random.randint(-5, 5),
                'diastolic_bp': 80 + random.randint(-3, 3)
            })
        
        return history[::-1]  # Return in chronological order

