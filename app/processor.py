"""
Detection Processor - Main processing loop
Combines camera capture, pose detection, fall detection, and alerts
"""
import threading
import time
from datetime import datetime
from typing import Optional

from app.ai.pose_detector import PoseDetector
from app.ai.fall_detector import EnhancedFallDetector, DetectionResult
from app.camera.capture import get_camera
from app.camera.recorder import get_recorder
from app.services.email_service import get_email_service
from app.sockets.events import broadcast_fall_alert, broadcast_detection_update


class DetectionProcessor:
    """
    Main detection processing loop.
    Runs in a background thread, processing frames and detecting falls.
    """
    
    def __init__(self, app=None, db=None):
        """
        Initialize the detection processor.
        
        Args:
            app: Flask application (for app context)
            db: SQLAlchemy database instance
        """
        self.app = app
        self.db = db
        self.pose_detector = None
        self.fall_detector = None
        self.camera = None
        self.recorder = None
        self.email_service = None
        
        self.running = False
        self.thread = None
        self.last_detection_result = None
        self.frames_processed = 0
        
    def start(self):
        """Start the detection processor thread."""
        if self.running:
            return
        
        print("🚀 Starting detection processor...")
        
        # Initialize components
        self.pose_detector = PoseDetector()
        self.fall_detector = EnhancedFallDetector()  # Use enhanced detector
        self.camera = get_camera()
        self.recorder = get_recorder()
        self.email_service = get_email_service()
        
        # Start camera
        if not self.camera.start():
            print("❌ Failed to start camera")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()
        
        print("✅ Detection processor started")
    
    def _process_loop(self):
        """Main processing loop."""
        while self.running:
            try:
                # Get frame from camera
                frame = self.camera.get_frame()
                
                if frame is None:
                    time.sleep(0.05)
                    continue
                
                # Process pose
                landmarks, annotated_frame = self.pose_detector.process_frame(frame)
                
                # Add frame to recorder buffer
                self.recorder.add_frame(annotated_frame)
                
                # Detect falls
                result, analysis = self.fall_detector.analyze(landmarks)
                self.last_detection_result = result
                self.frames_processed += 1
                
                # Handle detection result
                if result == DetectionResult.FALL_DETECTED:
                    self._handle_fall(analysis, alert_type='FALL')
                elif result == DetectionResult.PERSON_DOWN:
                    # Person fell and hasn't gotten up - more urgent!
                    self._handle_fall(analysis, alert_type='PERSON_DOWN', severity='CRITICAL')
                elif result == DetectionResult.BENDING_OVER:
                    # Log but don't alert
                    if self.frames_processed % 30 == 0:
                        print(f"👤 Bending detected - No alert (posture: {analysis.get('posture', 'unknown')})")
                
                # Broadcast detection update periodically
                if self.frames_processed % 10 == 0:
                    broadcast_detection_update({
                        'result': result.value,
                        'frames_processed': self.frames_processed,
                        'fps': self.camera.get_fps(),
                    })
                
                # Small delay to prevent CPU overload
                time.sleep(0.01)
                
            except Exception as e:
                print(f"❌ Processing error: {e}")
                time.sleep(0.1)
    
    def _handle_fall(self, analysis: dict, alert_type: str = 'FALL', severity: str = 'HIGH'):
        """Handle a detected fall or person down event."""
        if alert_type == 'PERSON_DOWN':
            print("🚨🚨 CRITICAL: Person has NOT GOTTEN UP! Sending urgent alert...")
            print(f"   Time down: {analysis.get('time_down', 0):.1f}s")
        else:
            print("🚨 FALL DETECTED! Processing alert...")
        
        print(f"   Posture: {analysis.get('posture', 'unknown')}")
        print(f"   Body Angle: {analysis.get('body_angle', 0):.1f}°")
        
        timestamp = datetime.utcnow()
        body_angle = analysis.get('body_angle', 0)
        velocity = analysis.get('hip_velocity', 0)
        posture = analysis.get('posture', 'unknown')
        time_down = analysis.get('time_down', 0)
        confidence = analysis.get('posture_confidence', 0)
        
        # Create description based on alert type
        if alert_type == 'PERSON_DOWN':
            description = f'⚠️ URGENT: Person down for {time_down:.0f}s and not responding. Posture: {posture}'
        else:
            description = f'Fall detected. Posture: {posture}, Body angle: {body_angle:.1f}°'
        
        # Trigger video recording
        video_path = self.recorder.trigger_recording()
        
        # Create alert in database
        alert_data = None
        if self.app and self.db:
            with self.app.app_context():
                from app.models.database import Alert
                
                alert = Alert(
                    timestamp=timestamp,
                    alert_type=alert_type,
                    severity=severity,
                    video_path=video_path,
                    location='Camera 1',
                    description=description,
                    body_angle=body_angle,
                    velocity=velocity,
                )
                self.db.session.add(alert)
                self.db.session.commit()
                
                alert_data = alert.to_dict()
                print(f"✅ Alert saved to database: ID {alert.id}")
        
        # Broadcast to connected clients
        broadcast_fall_alert({
            'id': alert_data['id'] if alert_data else None,
            'timestamp': timestamp.isoformat(),
            'alert_type': alert_type,
            'severity': severity,
            'posture': posture,
            'body_angle': body_angle,
            'time_down': time_down,
            'video_path': video_path,
        })
        
        # Send email notification
        email_sent = self.email_service.send_fall_alert(
            timestamp=timestamp,
            severity=severity,
            location='Camera 1',
            video_path=video_path,
            body_angle=body_angle,
            velocity=velocity,
        )
        
        # Update database with email status
        if self.app and self.db and alert_data:
            with self.app.app_context():
                from app.models.database import Alert
                alert = Alert.query.get(alert_data['id'])
                if alert:
                    alert.sent_to_email = email_sent
                    self.db.session.commit()
    
    def stop(self):
        """Stop the detection processor."""
        print("🛑 Stopping detection processor...")
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=3)
        
        if self.camera:
            self.camera.stop()
        
        if self.pose_detector:
            self.pose_detector.close()
        
        print("✅ Detection processor stopped")
    
    def get_status(self) -> dict:
        """Get current processor status."""
        return {
            'running': self.running,
            'frames_processed': self.frames_processed,
            'last_result': self.last_detection_result.value if self.last_detection_result else None,
            'camera_fps': self.camera.get_fps() if self.camera else 0,
        }


# Global processor instance
_processor: Optional[DetectionProcessor] = None


def get_processor() -> Optional[DetectionProcessor]:
    """Get the global processor instance."""
    return _processor


def create_processor(app, db) -> DetectionProcessor:
    """Create and return the detection processor."""
    global _processor
    _processor = DetectionProcessor(app, db)
    return _processor
