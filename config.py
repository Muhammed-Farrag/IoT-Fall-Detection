"""
NovaCare Fall Detection System - Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Flask Settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alerts.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Camera Settings
    CAMERA_RESOLUTION = (640, 480)
    CAMERA_FPS = 30
    USE_RASPBERRY_PI_CAMERA = os.getenv('USE_PI_CAMERA', 'false').lower() == 'true'
    
    # Raspberry Pi Camera Stream URL (when Pi runs as separate server)
    RASPI_STREAM_URL = os.getenv('RASPI_STREAM_URL', 'http://raspberrypi.local:8000/video_feed')
    
    # Fall Detection Settings
    FALL_VELOCITY_THRESHOLD = 0.15  # Vertical velocity threshold
    FALL_ANGLE_THRESHOLD = 45  # Body angle threshold in degrees
    FALL_DURATION_THRESHOLD = 0.5  # Seconds - quick drop = fall
    BUFFER_SECONDS_BEFORE = 5  # Seconds of video before fall
    BUFFER_SECONDS_AFTER = 10  # Seconds of video after fall
    
    # Email Settings (SMTP)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    ALERT_EMAIL_TO = os.getenv('ALERT_EMAIL_TO', '')
    EMAIL_ENABLED = bool(os.getenv('SMTP_USERNAME'))
    
    # Recording Storage
    RECORDINGS_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'recordings')
