"""
Vision Service Interface - Dependency Inversion Principle
Abstracts computer vision functionality for navigation assistance
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IVisionService(ABC):
    """
    Abstract interface for vision-based assistance.
    Implementations can use different CV backends (OpenCV, cloud APIs, etc.)
    """
    
    @abstractmethod
    def identify_object(self, image_data: bytes) -> Dict[str, Any]:
        """
        Identify objects in the provided image.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dictionary with identified objects and confidence scores
        """
        pass
    
    @abstractmethod
    def read_text(self, image_data: bytes) -> Dict[str, Any]:
        """
        Extract and read text from an image (OCR).
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dictionary with extracted text and bounding boxes
        """
        pass
    
    @abstractmethod
    def describe_scene(self, image_data: bytes) -> Dict[str, Any]:
        """
        Generate a natural language description of the scene.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dictionary with scene description
        """
        pass
    
    @abstractmethod
    def detect_obstacles(self, depth_data: bytes) -> Dict[str, Any]:
        """
        Detect obstacles for navigation assistance.
        
        Args:
            depth_data: Depth sensor data
            
        Returns:
            Dictionary with obstacle locations and distances
        """
        pass
    
    @abstractmethod
    def track_person(self, video_frame: bytes, person_id: str) -> Dict[str, Any]:
        """
        Track a specific person for follow mode.
        
        Args:
            video_frame: Current video frame
            person_id: Identifier for the person to track
            
        Returns:
            Dictionary with tracking status and position
        """
        pass

