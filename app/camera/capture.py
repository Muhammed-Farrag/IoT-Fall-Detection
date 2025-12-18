"""
Camera Capture Module
Supports: Raspberry Pi Camera stream, Local webcam
"""
import cv2
import numpy as np
import threading
import time
import requests
from typing import Optional, Generator
from config import Config


class CameraCapture:
    """
    Camera capture supporting Raspberry Pi camera stream and local webcam.
    
    When connected to a Raspberry Pi running the camera server,
    it fetches the video stream over HTTP.
    """
    
    def __init__(self, use_pi_camera: bool = None, 
                 pi_stream_url: str = None,
                 resolution: tuple = None):
        """
        Initialize camera capture.
        
        Args:
            use_pi_camera: Use Raspberry Pi camera stream
            pi_stream_url: URL of the Pi camera stream
            resolution: (width, height) tuple
        """
        self.use_pi_camera = use_pi_camera if use_pi_camera is not None else Config.USE_RASPBERRY_PI_CAMERA
        self.pi_stream_url = pi_stream_url or Config.RASPI_STREAM_URL
        self.resolution = resolution or Config.CAMERA_RESOLUTION
        
        self.cap = None
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None
        self.last_frame_time = 0
        self.fps = 0
        
    def start(self) -> bool:
        """Start the camera capture thread."""
        if self.running:
            return True
            
        if self.use_pi_camera:
            # Will fetch from Raspberry Pi stream
            print(f"📡 Using Raspberry Pi camera stream: {self.pi_stream_url}")
            self.running = True
            self.thread = threading.Thread(target=self._capture_from_stream, daemon=True)
        else:
            # Local webcam
            print("📷 Using local webcam")
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("❌ Failed to open webcam")
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self.running = True
            self.thread = threading.Thread(target=self._capture_from_webcam, daemon=True)
        
        self.thread.start()
        return True
    
    def _capture_from_webcam(self):
        """Capture frames from local webcam."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
                    self._update_fps()
            time.sleep(0.01)  # ~100 FPS max
    
    def _capture_from_stream(self):
        """Capture frames from Raspberry Pi MJPEG stream."""
        while self.running:
            try:
                # Fetch MJPEG stream
                response = requests.get(self.pi_stream_url, stream=True, timeout=5)
                bytes_data = bytes()
                
                for chunk in response.iter_content(chunk_size=1024):
                    if not self.running:
                        break
                    bytes_data += chunk
                    
                    # Look for JPEG frame boundaries
                    a = bytes_data.find(b'\xff\xd8')  # JPEG start
                    b = bytes_data.find(b'\xff\xd9')  # JPEG end
                    
                    if a != -1 and b != -1:
                        jpg = bytes_data[a:b+2]
                        bytes_data = bytes_data[b+2:]
                        
                        # Decode JPEG
                        frame = cv2.imdecode(
                            np.frombuffer(jpg, dtype=np.uint8), 
                            cv2.IMREAD_COLOR
                        )
                        
                        if frame is not None:
                            with self.lock:
                                self.frame = frame
                                self._update_fps()
                                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Stream error: {e}. Retrying in 2s...")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Capture error: {e}")
                time.sleep(1)
    
    def _update_fps(self):
        """Calculate FPS."""
        current_time = time.time()
        if self.last_frame_time > 0:
            delta = current_time - self.last_frame_time
            if delta > 0:  # Prevent division by zero
                self.fps = 1.0 / delta
        self.last_frame_time = current_time
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get the current frame (thread-safe)."""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
    
    def get_fps(self) -> float:
        """Get current FPS."""
        return self.fps
    
    def generate_frames(self) -> Generator[bytes, None, None]:
        """Generate JPEG frames for streaming."""
        while self.running:
            frame = self.get_frame()
            if frame is not None:
                # Encode as JPEG
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.033)  # ~30 FPS
    
    def stop(self):
        """Stop the camera capture."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        print("📷 Camera stopped")
    
    def is_running(self) -> bool:
        """Check if camera is running."""
        return self.running


# Global camera instance
_camera_instance: Optional[CameraCapture] = None


def get_camera() -> CameraCapture:
    """Get or create the global camera instance."""
    global _camera_instance
    if _camera_instance is None:
        _camera_instance = CameraCapture()
    return _camera_instance
