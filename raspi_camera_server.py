"""
Raspberry Pi Camera Server - Enhanced
Streams high-quality video to the NovaCare Fall Detection System
"""
import io
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# Camera settings
RESOLUTION = (1280, 720)  # HD resolution (was 640x480)
QUALITY = 90  # JPEG quality (higher = better quality, was 80)
FPS = 30

# Try to import picamera2, fallback to opencv
try:
    from picamera2 import Picamera2
    from libcamera import controls
    USING_PICAMERA = True
except ImportError:
    import cv2
    USING_PICAMERA = False
    print("⚠️ picamera2 not available, using OpenCV fallback")


class StreamingOutput(io.BufferedIOBase):
    """Buffer for camera frames."""
    
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()
    
    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
        return len(buf)


class StreamingHandler(BaseHTTPRequestHandler):
    """HTTP handler for MJPEG streaming with CORS support."""
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/video_feed')
            self.end_headers()
            
        elif self.path == '/video_feed':
            self.send_response(200)
            self.send_header('Age', '0')
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            # CORS headers for dashboard access
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    
                    if frame is None:
                        continue
                        
                    self.wfile.write(b'--FRAME\r\n')
                    self.wfile.write(b'Content-Type: image/jpeg\r\n')
                    self.wfile.write(f'Content-Length: {len(frame)}\r\n\r\n'.encode())
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                    
            except Exception as e:
                print(f'Client disconnected: {e}')
                
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status": "ok", "camera": "active"}')
            
        else:
            self.send_error(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads."""
    allow_reuse_address = True
    daemon_threads = True


def start_camera_opencv():
    """Start camera using OpenCV (fallback)."""
    global output
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])
    cap.set(cv2.CAP_PROP_FPS, FPS)
    
    print(f"📷 Camera started (OpenCV) - {RESOLUTION[0]}x{RESOLUTION[1]} @ {FPS}fps")
    
    while True:
        ret, frame = cap.read()
        if ret:
            # Encode as JPEG with high quality
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, QUALITY])
            with output.condition:
                output.frame = buffer.tobytes()
                output.condition.notify_all()
        time.sleep(1.0 / FPS)


def start_camera_picamera():
    """Start camera using PiCamera2 with enhanced settings."""
    global output
    import cv2
    
    picam2 = Picamera2()
    
    # Configure for high quality video
    config = picam2.create_video_configuration(
        main={"size": RESOLUTION, "format": "RGB888"},
        controls={
            "FrameRate": FPS,
        },
        buffer_count=4
    )
    picam2.configure(config)
    
    # Set camera controls for better image
    picam2.set_controls({
        "AeEnable": True,  # Auto exposure
        "AwbEnable": True,  # Auto white balance
        "NoiseReductionMode": 2,  # High quality noise reduction
    })
    
    picam2.start()
    print(f"📷 Camera started (PiCamera2) - {RESOLUTION[0]}x{RESOLUTION[1]} @ {FPS}fps")
    print(f"   Quality: {QUALITY}%")
    
    try:
        while True:
            # Capture frame
            frame = picam2.capture_array()
            
            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Encode as high quality JPEG
            _, buffer = cv2.imencode('.jpg', frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, QUALITY])
            
            with output.condition:
                output.frame = buffer.tobytes()
                output.condition.notify_all()
            
            time.sleep(1.0 / FPS)
    finally:
        picam2.stop()


if __name__ == '__main__':
    output = StreamingOutput()
    PORT = 8000
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║     📹 Raspberry Pi Camera Server - Enhanced              ║
    ║     ──────────────────────────────────────────────────    ║
    ║     Resolution: {RESOLUTION[0]}x{RESOLUTION[1]} @ {FPS}fps                      ║
    ║     Quality: {QUALITY}%                                          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Start camera thread
    if USING_PICAMERA:
        camera_thread = threading.Thread(target=start_camera_picamera, daemon=True)
    else:
        camera_thread = threading.Thread(target=start_camera_opencv, daemon=True)
    
    camera_thread.start()
    time.sleep(2)  # Wait for camera to initialize
    
    # Start HTTP server
    server = ThreadedHTTPServer(('0.0.0.0', PORT), StreamingHandler)
    print(f"🌐 Stream: http://0.0.0.0:{PORT}/video_feed")
    print(f"   Health: http://0.0.0.0:{PORT}/health")
    print("\nPress Ctrl+C to stop...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()
