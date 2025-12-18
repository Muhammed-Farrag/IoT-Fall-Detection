"""
API Routes for Fall Detection System
RESTful endpoints for dashboard data
"""
from flask import Blueprint, jsonify, request, Response
from datetime import datetime, timedelta
from app import db
from app.models.database import Alert, SystemStats
from app.camera.capture import get_camera

api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint."""
    camera = get_camera()
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'camera_running': camera.is_running() if camera else False,
        'fps': camera.get_fps() if camera else 0,
    })


@api_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get all alerts with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    severity = request.args.get('severity', None)
    acknowledged = request.args.get('acknowledged', None)
    
    query = Alert.query.order_by(Alert.timestamp.desc())
    
    # Filter by severity
    if severity:
        query = query.filter(Alert.severity == severity.upper())
    
    # Filter by acknowledged status
    if acknowledged is not None:
        ack_bool = acknowledged.lower() == 'true'
        query = query.filter(Alert.acknowledged == ack_bool)
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'alerts': [alert.to_dict() for alert in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
    })


@api_bp.route('/alerts/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get a specific alert by ID."""
    alert = Alert.query.get_or_404(alert_id)
    return jsonify(alert.to_dict())


@api_bp.route('/alerts/<int:alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Mark an alert as acknowledged."""
    alert = Alert.query.get_or_404(alert_id)
    
    data = request.get_json() or {}
    acknowledged_by = data.get('acknowledged_by', 'Admin')
    
    alert.acknowledged = True
    alert.acknowledged_at = datetime.utcnow()
    alert.acknowledged_by = acknowledged_by
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Alert acknowledged',
        'alert': alert.to_dict()
    })


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics."""
    # Time ranges
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)
    
    # Count alerts
    total_alerts = Alert.query.count()
    unacked_alerts = Alert.query.filter_by(acknowledged=False).count()
    today_alerts = Alert.query.filter(Alert.timestamp >= today_start).count()
    week_alerts = Alert.query.filter(Alert.timestamp >= week_ago).count()
    
    # Get alerts by severity
    high_severity = Alert.query.filter_by(severity='HIGH').count()
    medium_severity = Alert.query.filter_by(severity='MEDIUM').count()
    low_severity = Alert.query.filter_by(severity='LOW').count()
    
    # Get camera status
    camera = get_camera()
    camera_status = 'active' if camera and camera.is_running() else 'inactive'
    
    # Calculate uptime (simplified - based on camera running time)
    uptime = 99.8  # Placeholder - would calculate from logs in production
    
    return jsonify({
        'total_alerts': total_alerts,
        'unacknowledged_alerts': unacked_alerts,
        'today_alerts': today_alerts,
        'week_alerts': week_alerts,
        'alerts_by_severity': {
            'high': high_severity,
            'medium': medium_severity,
            'low': low_severity,
        },
        'camera_status': camera_status,
        'camera_fps': camera.get_fps() if camera else 0,
        'device_uptime': uptime,
        'mqtt_status': 'connected',  # Placeholder
    })


@api_bp.route('/stats/daily', methods=['GET'])
def get_daily_stats():
    """Get daily statistics for charts."""
    days = request.args.get('days', 7, type=int)
    now = datetime.utcnow()
    
    daily_data = []
    for i in range(days - 1, -1, -1):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        count = Alert.query.filter(
            Alert.timestamp >= day_start,
            Alert.timestamp < day_end
        ).count()
        
        daily_data.append({
            'date': day_start.strftime('%a'),
            'count': count,
        })
    
    return jsonify({'daily_stats': daily_data})


@api_bp.route('/video/live', methods=['GET'])
def video_feed():
    """Live video stream endpoint (MJPEG)."""
    camera = get_camera()
    if not camera or not camera.is_running():
        return jsonify({'error': 'Camera not available'}), 503
    
    return Response(
        camera.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@api_bp.route('/video/pi-stream', methods=['GET'])
def pi_video_proxy():
    """Proxy the Raspberry Pi camera stream to avoid CORS issues."""
    import requests
    from config import Config
    
    pi_url = Config.RASPI_STREAM_URL
    
    def generate():
        try:
            with requests.get(pi_url, stream=True, timeout=10) as response:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        yield chunk
        except Exception as e:
            print(f"Pi stream proxy error: {e}")
            return
    
    return Response(
        generate(),
        mimetype='multipart/x-mixed-replace; boundary=FRAME'
    )


@api_bp.route('/detection/status', methods=['GET'])
def detection_status():
    """Get current detection status."""
    # This would be updated by the detection thread
    return jsonify({
        'status': 'running',
        'last_detection': None,  # Would be populated with last detection result
        'persons_detected': 0,
    })
