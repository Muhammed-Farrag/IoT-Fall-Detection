"""
Advanced Fall Detection with Full Body Posture Analysis
Analyzes entire body posture and detects if person stays down
"""
import time
import numpy as np
from collections import deque
from typing import Dict, Optional, Tuple, List
from enum import Enum


class DetectionResult(Enum):
    """Fall detection result types."""
    NORMAL = "normal"
    BENDING_OVER = "bending_over"
    FALL_DETECTED = "fall_detected"
    PERSON_DOWN = "person_down"  # Person has fallen and not gotten up
    NO_PERSON = "no_person"


class BodyPosture(Enum):
    """Body posture states."""
    STANDING = "standing"
    SITTING = "sitting"
    BENDING = "bending"
    LYING_DOWN = "lying_down"
    FALLING = "falling"
    UNKNOWN = "unknown"


class FullBodyFallDetector:
    """
    Advanced fall detection using full body posture analysis.
    
    Analyzes:
    1. Body orientation (vertical vs horizontal)
    2. Limb positions relative to torso
    3. Height of body from ground
    4. Time spent in fallen position
    5. Movement patterns (controlled vs uncontrolled)
    """
    
    # MediaPipe landmark indices
    NOSE = 0
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    
    def __init__(self, 
                 fallen_timeout: float = 5.0,  # Seconds before "stayed down" alert
                 history_seconds: float = 3.0,
                 fps: int = 30):
        """
        Initialize the full body fall detector.
        
        Args:
            fallen_timeout: Seconds to wait before alerting person stayed down
            history_seconds: Seconds of pose history to keep
            fps: Expected frames per second
        """
        self.fallen_timeout = fallen_timeout
        self.history_size = int(history_seconds * fps)
        
        # Pose history
        self.pose_history = deque(maxlen=self.history_size)
        self.posture_history = deque(maxlen=self.history_size)
        self.timestamps = deque(maxlen=self.history_size)
        
        # Fall tracking
        self.fall_detected_time = None
        self.person_is_down = False
        self.down_since = None
        self.last_standing_time = None
        self.cooldown_until = 0
        
        # Results
        self.last_result = DetectionResult.NORMAL
        self.last_posture = BodyPosture.UNKNOWN
        
    def analyze(self, landmarks: Optional[Dict]) -> Tuple[DetectionResult, Dict]:
        """
        Analyze full body posture to detect falls.
        
        Args:
            landmarks: Dictionary of body landmarks from PoseDetector
            
        Returns:
            Tuple of (DetectionResult, analysis_data)
        """
        current_time = time.time()
        analysis = {
            'posture': 'unknown',
            'confidence': 0,
            'time_down': 0,
            'body_horizontal': False,
        }
        
        # Cooldown check
        if current_time < self.cooldown_until:
            return self.last_result, {'status': 'cooldown'}
        
        if landmarks is None:
            # Person left frame - reset if they were down
            if self.person_is_down:
                self._reset_fall_state()
            return DetectionResult.NO_PERSON, {'status': 'no_person'}
        
        # Get body posture
        posture, posture_confidence = self._analyze_posture(landmarks)
        analysis['posture'] = posture.value
        analysis['posture_confidence'] = posture_confidence
        
        # Update history
        self.pose_history.append(landmarks)
        self.posture_history.append(posture)
        self.timestamps.append(current_time)
        
        self.last_posture = posture
        
        # Track standing time
        if posture == BodyPosture.STANDING:
            self.last_standing_time = current_time
        
        # Analyze body metrics
        body_metrics = self._calculate_body_metrics(landmarks)
        analysis.update(body_metrics)
        
        # FALL DETECTION LOGIC
        result = self._detect_fall_state(posture, body_metrics, current_time, analysis)
        
        self.last_result = result
        return result, analysis
    
    def _analyze_posture(self, landmarks: Dict) -> Tuple[BodyPosture, float]:
        """
        Analyze full body to determine current posture.
        
        Returns:
            Tuple of (BodyPosture, confidence)
        """
        # Get key body points
        nose = landmarks.get('nose', {})
        center_shoulder = landmarks.get('center_shoulder', {})
        center_hip = landmarks.get('center_hip', {})
        left_knee = landmarks.get('left_knee', {})
        right_knee = landmarks.get('right_knee', {})
        left_ankle = landmarks.get('left_ankle', {})
        right_ankle = landmarks.get('right_ankle', {})
        
        # Y positions (higher value = lower in frame)
        nose_y = nose.get('y', 0.2)
        shoulder_y = center_shoulder.get('y', 0.3)
        hip_y = center_hip.get('y', 0.5)
        knee_y = (left_knee.get('y', 0.7) + right_knee.get('y', 0.7)) / 2
        ankle_y = (left_ankle.get('y', 0.9) + right_ankle.get('y', 0.9)) / 2
        
        # X positions for horizontal spread
        shoulder_x = center_shoulder.get('x', 0.5)
        hip_x = center_hip.get('x', 0.5)
        
        # Calculate body orientation
        body_angle = landmarks.get('body_angle', 0)
        
        # Calculate vertical span of body
        body_height = ankle_y - nose_y
        
        # Calculate if body is horizontal (shoulders and hips at similar Y)
        torso_horizontal = abs(shoulder_y - hip_y) < 0.15
        
        # Check if head is at level of or below hips
        head_below_normal = nose_y > hip_y - 0.1
        
        # Posture classification
        confidence = 0.7
        
        # LYING DOWN: Body horizontal, minimal vertical span
        if torso_horizontal and body_height < 0.4 and head_below_normal:
            return BodyPosture.LYING_DOWN, 0.85
        
        # STANDING: Normal vertical alignment, full body height
        if body_height > 0.5 and body_angle < 30 and not head_below_normal:
            if abs(shoulder_y - hip_y) > 0.1:  # Shoulders above hips
                return BodyPosture.STANDING, 0.9
        
        # SITTING: Hips low, but knees bent
        if hip_y > 0.6 and knee_y > hip_y and body_angle < 40:
            return BodyPosture.SITTING, 0.75
        
        # BENDING: Tilted but controlled
        if body_angle > 40 and body_angle < 80 and body_height > 0.3:
            return BodyPosture.BENDING, 0.8
        
        # FALLING: Rapid transition detected (checked via history)
        if len(self.posture_history) >= 5:
            recent_postures = list(self.posture_history)[-5:]
            if recent_postures[0] == BodyPosture.STANDING:
                if body_angle > 50 or torso_horizontal:
                    return BodyPosture.FALLING, 0.8
        
        return BodyPosture.UNKNOWN, 0.5
    
    def _calculate_body_metrics(self, landmarks: Dict) -> Dict:
        """Calculate detailed body metrics."""
        metrics = {}
        
        # Get positions
        nose = landmarks.get('nose', {})
        center_shoulder = landmarks.get('center_shoulder', {})
        center_hip = landmarks.get('center_hip', {})
        left_wrist = landmarks.get('left_wrist', {})
        right_wrist = landmarks.get('right_wrist', {})
        
        # Body angle
        metrics['body_angle'] = landmarks.get('body_angle', 0)
        
        # Vertical positions
        metrics['head_y'] = nose.get('y', 0.2)
        metrics['shoulder_y'] = center_shoulder.get('y', 0.3)
        metrics['hip_y'] = center_hip.get('y', 0.5)
        
        # Check if hands are reaching (trying to catch self)
        avg_wrist_y = (left_wrist.get('y', 0.5) + right_wrist.get('y', 0.5)) / 2
        metrics['hands_extended'] = avg_wrist_y > center_hip.get('y', 0.5)
        
        # Body horizontal check
        shoulder_hip_diff = abs(center_shoulder.get('y', 0.3) - center_hip.get('y', 0.5))
        metrics['body_horizontal'] = shoulder_hip_diff < 0.15
        
        # Head position relative to hip
        metrics['head_at_hip_level'] = nose.get('y', 0.2) > center_hip.get('y', 0.5) - 0.15
        
        return metrics
    
    def _detect_fall_state(self, posture: BodyPosture, metrics: Dict, 
                           current_time: float, analysis: Dict) -> DetectionResult:
        """
        Determine fall detection result based on posture and metrics.
        """
        # Check if person is lying down or in fallen position
        is_down = (
            posture == BodyPosture.LYING_DOWN or
            (metrics.get('body_horizontal', False) and metrics.get('head_at_hip_level', False))
        )
        
        # DETECT INITIAL FALL
        if posture == BodyPosture.FALLING or (is_down and not self.person_is_down):
            # Check if this is a new fall (was standing recently)
            if self.last_standing_time:
                time_since_standing = current_time - self.last_standing_time
                if time_since_standing < 2.0:  # Fell within 2 seconds of standing
                    self.fall_detected_time = current_time
                    self.person_is_down = True
                    self.down_since = current_time
                    analysis['reason'] = 'sudden_fall_from_standing'
                    return DetectionResult.FALL_DETECTED
        
        # PERSON IS DOWN - Check how long
        if is_down:
            if not self.person_is_down:
                self.person_is_down = True
                self.down_since = current_time
            
            time_down = current_time - self.down_since if self.down_since else 0
            analysis['time_down'] = time_down
            
            # Alert if person hasn't gotten up for too long
            if time_down > self.fallen_timeout:
                if self.fall_detected_time is None:  # First time detecting they're stuck down
                    self.fall_detected_time = current_time
                    analysis['reason'] = 'person_stayed_down'
                    self.cooldown_until = current_time + 30  # 30 second cooldown
                    return DetectionResult.PERSON_DOWN
        
        # PERSON GOT UP - Reset
        if posture == BodyPosture.STANDING and self.person_is_down:
            self._reset_fall_state()
            analysis['reason'] = 'person_recovered'
        
        # BENDING (NOT FALL)
        if posture == BodyPosture.BENDING:
            return DetectionResult.BENDING_OVER
        
        return DetectionResult.NORMAL
    
    def _reset_fall_state(self):
        """Reset fall tracking state."""
        self.person_is_down = False
        self.down_since = None
        self.fall_detected_time = None
    
    def reset(self):
        """Full reset of detector."""
        self.pose_history.clear()
        self.posture_history.clear()
        self.timestamps.clear()
        self._reset_fall_state()
        self.last_standing_time = None
        self.last_result = DetectionResult.NORMAL
        self.last_posture = BodyPosture.UNKNOWN


# Keep backward compatibility
EnhancedFallDetector = FullBodyFallDetector
