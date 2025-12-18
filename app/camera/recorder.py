"""
Video Recorder Module
Records fall events with buffer before and after detection
"""
import cv2
import os
import threading
import time
from collections import deque
from datetime import datetime
from typing import Optional
from config import Config


class VideoRecorder:
    """
    Records video with a rolling buffer.
    Saves footage before and after fall detection.
    """
    
    def __init__(self, 
                 buffer_seconds_before: int = None,
                 buffer_seconds_after: int = None,
                 fps: int = 30,
                 output_folder: str = None):
        """
        Initialize the video recorder.
        
        Args:
            buffer_seconds_before: Seconds of video to keep before fall
            buffer_seconds_after: Seconds of video to record after fall
            fps: Frames per second
            output_folder: Folder to save recordings
        """
        self.buffer_before = buffer_seconds_before or Config.BUFFER_SECONDS_BEFORE
        self.buffer_after = buffer_seconds_after or Config.BUFFER_SECONDS_AFTER
        self.fps = fps
        self.output_folder = output_folder or Config.RECORDINGS_FOLDER
        
        # Calculate buffer size
        self.buffer_size = self.buffer_before * fps
        self.frame_buffer = deque(maxlen=self.buffer_size)
        
        # Recording state
        self.is_recording_after = False
        self.after_frames_count = 0
        self.after_frames_target = self.buffer_after * fps
        self.current_recording = []
        self.lock = threading.Lock()
        
        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)
        
    def add_frame(self, frame):
        """Add a frame to the rolling buffer."""
        with self.lock:
            self.frame_buffer.append(frame.copy())
            
            # If we're recording after a fall event
            if self.is_recording_after:
                self.current_recording.append(frame.copy())
                self.after_frames_count += 1
                
                if self.after_frames_count >= self.after_frames_target:
                    self._save_recording()
    
    def trigger_recording(self) -> str:
        """
        Trigger a recording on fall detection.
        Returns the future path of the recording.
        """
        with self.lock:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fall_{timestamp}.mp4"
            filepath = os.path.join(self.output_folder, filename)
            
            # Start with buffered frames (before the fall)
            self.current_recording = list(self.frame_buffer)
            self.is_recording_after = True
            self.after_frames_count = 0
            
            print(f"🎬 Recording triggered: {filename}")
            print(f"   Buffer frames: {len(self.current_recording)}")
            
            return filepath
    
    def _save_recording(self):
        """Save the current recording to file."""
        if not self.current_recording:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fall_{timestamp}.mp4"
        filepath = os.path.join(self.output_folder, filename)
        
        # Get frame dimensions
        height, width = self.current_recording[0].shape[:2]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filepath, fourcc, self.fps, (width, height))
        
        # Write all frames
        for frame in self.current_recording:
            out.write(frame)
        
        out.release()
        
        # Reset state
        self.is_recording_after = False
        self.after_frames_count = 0
        self.current_recording = []
        
        print(f"✅ Recording saved: {filepath}")
        print(f"   Total frames: {len(self.current_recording)}")
        
        return filepath
    
    def get_latest_recording(self) -> Optional[str]:
        """Get the path to the most recent recording."""
        recordings = [f for f in os.listdir(self.output_folder) if f.endswith('.mp4')]
        if not recordings:
            return None
        
        recordings.sort(reverse=True)
        return os.path.join(self.output_folder, recordings[0])


# Global recorder instance
_recorder_instance: Optional[VideoRecorder] = None


def get_recorder() -> VideoRecorder:
    """Get or create the global recorder instance."""
    global _recorder_instance
    if _recorder_instance is None:
        _recorder_instance = VideoRecorder()
    return _recorder_instance
