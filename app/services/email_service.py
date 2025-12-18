"""
Email Notification Service
Sends alerts via SMTP
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Optional
from config import Config


class EmailService:
    """Email notification service for fall alerts."""
    
    def __init__(self):
        """Initialize email service with config."""
        self.server = Config.SMTP_SERVER
        self.port = Config.SMTP_PORT
        self.username = Config.SMTP_USERNAME
        self.password = Config.SMTP_PASSWORD
        self.to_email = Config.ALERT_EMAIL_TO
        self.enabled = Config.EMAIL_ENABLED
        
    def send_fall_alert(self, 
                        timestamp: datetime,
                        severity: str = 'HIGH',
                        location: str = 'Camera 1',
                        video_path: Optional[str] = None,
                        body_angle: Optional[float] = None,
                        velocity: Optional[float] = None) -> bool:
        """
        Send a fall detection alert email.
        
        Args:
            timestamp: Time of the fall
            severity: Alert severity (HIGH, MEDIUM, LOW)
            location: Camera location
            video_path: Path to recorded video (optional)
            body_angle: Detected body angle
            velocity: Detected fall velocity
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.enabled:
            print("⚠️ Email not configured. Skipping notification.")
            return False
        
        if not self.to_email:
            print("⚠️ No recipient email configured.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = self.to_email
            msg['Subject'] = f"🚨 FALL ALERT - {severity} Priority - NovaCare System"
            
            # Email body
            body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #e74a3b, #c0392b); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f8f9fc; padding: 20px; border: 1px solid #e3e6f0; }}
        .alert-box {{ background: white; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #e74a3b; }}
        .field {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #5a5c69; }}
        .value {{ color: #1a1d23; }}
        .footer {{ background: #1a1d23; color: white; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; }}
        .btn {{ display: inline-block; background: #4e73df; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 Fall Detection Alert</h1>
            <p>NovaCare Emergency Response System</p>
        </div>
        <div class="content">
            <div class="alert-box">
                <div class="field">
                    <span class="label">⏰ Time:</span>
                    <span class="value">{timestamp.strftime('%Y-%m-%d %H:%M:%S')}</span>
                </div>
                <div class="field">
                    <span class="label">📍 Location:</span>
                    <span class="value">{location}</span>
                </div>
                <div class="field">
                    <span class="label">⚠️ Severity:</span>
                    <span class="value" style="color: #e74a3b; font-weight: bold;">{severity}</span>
                </div>
                {f'<div class="field"><span class="label">📐 Body Angle:</span><span class="value">{body_angle:.1f}°</span></div>' if body_angle else ''}
                {f'<div class="field"><span class="label">⚡ Fall Velocity:</span><span class="value">{velocity:.3f}</span></div>' if velocity else ''}
            </div>
            
            <h3>⚡ Immediate Actions Required:</h3>
            <ol>
                <li>Check on the person immediately</li>
                <li>Call emergency services if needed: <strong>911</strong></li>
                <li>Review the recorded footage in the dashboard</li>
            </ol>
            
            <p style="text-align: center; margin-top: 20px;">
                <a href="http://localhost:5000/dashboard" class="btn">View Dashboard</a>
            </p>
        </div>
        <div class="footer">
            <p>NovaCare Fall Detection System</p>
            <small>This is an automated alert. Please respond immediately.</small>
        </div>
    </div>
</body>
</html>
"""
            
            msg.attach(MIMEText(body, 'html'))
            
            # Attach video if available
            if video_path and os.path.exists(video_path):
                with open(video_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(video_path)}'
                )
                msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"✅ Alert email sent to {self.to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection."""
        if not self.enabled:
            return False
        
        try:
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
            return True
        except Exception as e:
            print(f"❌ SMTP connection test failed: {e}")
            return False


# Global email service instance
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """Get or create the global email service instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
