"""
Pose Detection using MediaPipe
Extracts body landmarks for fall detection analysis
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, List, Tuple


class PoseDetector:
    """MediaPipe Pose detector wrapper for extracting body landmarks."""
    
    # Key landmark indices
    LANDMARKS = {
        'nose': 0,
        'left_shoulder': 11,
        'right_shoulder': 12,
        'left_hip': 23,
        'right_hip': 24,
        'left_knee': 25,
        'right_knee': 26,
        'left_ankle': 27,
        'right_ankle': 28,
    }
    
    def __init__(self, min_detection_confidence: float = 0.5, 
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the pose detector.
        
        Args:
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
    def process_frame(self, frame: np.ndarray) -> Tuple[Optional[Dict], np.ndarray]:
        """
        Process a video frame and extract pose landmarks.
        
        Args:
            frame: BGR image from camera
            
        Returns:
            Tuple of (landmarks dict, annotated frame)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        # Draw landmarks on frame
        rgb_frame.flags.writeable = True
        annotated_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing.DrawingSpec(
                    color=(0, 255, 0), thickness=2, circle_radius=3
                ),
                connection_drawing_spec=self.mp_drawing.DrawingSpec(
                    color=(255, 255, 255), thickness=2
                )
            )
            
            landmarks = self._extract_landmarks(results.pose_landmarks, frame.shape)
            return landmarks, annotated_frame
        
        return None, annotated_frame
    
    def _extract_landmarks(self, pose_landmarks, frame_shape: Tuple[int, int, int]) -> Dict:
        """
        Extract relevant landmarks as normalized and pixel coordinates.
        
        Args:
            pose_landmarks: MediaPipe pose landmarks
            frame_shape: Shape of the frame (height, width, channels)
            
        Returns:
            Dictionary with landmark positions
        """
        h, w, _ = frame_shape
        landmarks = {}
        
        for name, idx in self.LANDMARKS.items():
            landmark = pose_landmarks.landmark[idx]
            landmarks[name] = {
                'x': landmark.x,  # Normalized 0-1
                'y': landmark.y,  # Normalized 0-1
                'z': landmark.z,  # Depth
                'visibility': landmark.visibility,
                'pixel_x': int(landmark.x * w),
                'pixel_y': int(landmark.y * h),
            }
        
        # Calculate derived values
        landmarks['center_shoulder'] = self._midpoint(
            landmarks['left_shoulder'], landmarks['right_shoulder']
        )
        landmarks['center_hip'] = self._midpoint(
            landmarks['left_hip'], landmarks['right_hip']
        )
        
        # Calculate body angle (degrees from vertical)
        landmarks['body_angle'] = self._calculate_body_angle(
            landmarks['center_shoulder'], landmarks['center_hip']
        )
        
        return landmarks
    
    def _midpoint(self, p1: Dict, p2: Dict) -> Dict:
        """Calculate midpoint between two landmarks."""
        return {
            'x': (p1['x'] + p2['x']) / 2,
            'y': (p1['y'] + p2['y']) / 2,
            'z': (p1['z'] + p2['z']) / 2,
            'visibility': min(p1['visibility'], p2['visibility']),
        }
    
    def _calculate_body_angle(self, shoulder: Dict, hip: Dict) -> float:
        """
        Calculate body angle from vertical.
        0° = standing upright, 90° = horizontal
        """
        dx = shoulder['x'] - hip['x']
        dy = shoulder['y'] - hip['y']
        
        # Angle from vertical (y-axis points down in image coordinates)
        angle_rad = np.arctan2(abs(dx), abs(dy))
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
    
    def close(self):
        """Release resources."""
        self.pose.close()
