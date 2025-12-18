"""
Database Models for Fall Detection System
"""
from datetime import datetime
from app import db


class Alert(db.Model):
    """Alert model for storing fall detection events."""
    
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    alert_type = db.Column(db.String(50), default='FALL', nullable=False)
    severity = db.Column(db.String(20), default='HIGH', nullable=False)
    video_path = db.Column(db.String(255), nullable=True)
    acknowledged = db.Column(db.Boolean, default=False, nullable=False)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    acknowledged_by = db.Column(db.String(100), nullable=True)
    sent_to_email = db.Column(db.Boolean, default=False, nullable=False)
    location = db.Column(db.String(100), default='Camera 1', nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Analysis data
    body_angle = db.Column(db.Float, nullable=True)
    velocity = db.Column(db.Float, nullable=True)
    
    def to_dict(self):
        """Convert alert to dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'video_path': self.video_path,
            'video_url': f'/static/recordings/{self.video_path.split("/")[-1]}' if self.video_path else None,
            'acknowledged': self.acknowledged,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            'acknowledged_by': self.acknowledged_by,
            'sent_to_email': self.sent_to_email,
            'location': self.location,
            'description': self.description,
            'body_angle': self.body_angle,
            'velocity': self.velocity,
        }
    
    def __repr__(self):
        return f'<Alert {self.id}: {self.alert_type} at {self.timestamp}>'


class SystemStats(db.Model):
    """System statistics model."""
    
    __tablename__ = 'system_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cpu_usage = db.Column(db.Float, nullable=True)
    memory_usage = db.Column(db.Float, nullable=True)
    camera_status = db.Column(db.String(20), default='unknown')
    detection_rate = db.Column(db.Float, nullable=True)
    fps = db.Column(db.Float, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'camera_status': self.camera_status,
            'detection_rate': self.detection_rate,
            'fps': self.fps,
        }
