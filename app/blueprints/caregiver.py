"""
Caregiver Dashboard Blueprint
Single Responsibility: Only handles HTTP routing for caregiver dashboard
"""
from flask import Blueprint, render_template, jsonify, request
from app.services import CaregiverService

# Create blueprint
caregiver_bp = Blueprint('caregiver', __name__, url_prefix='/caregiver')

# Dependency Injection
caregiver_service = CaregiverService()


@caregiver_bp.route('/')
@caregiver_bp.route('/dashboard')
def dashboard():
    """Render the caregiver dashboard."""
    return render_template('caregiver/dashboard.html')


@caregiver_bp.route('/api/patient/status/<patient_id>', methods=['GET'])
def get_patient_status(patient_id):
    """Get patient status."""
    result = caregiver_service.get_patient_status(patient_id)
    return jsonify(result)


@caregiver_bp.route('/api/patient/location/<patient_id>', methods=['GET'])
def get_location(patient_id):
    """Get patient location."""
    result = caregiver_service.get_location(patient_id)
    return jsonify(result)


@caregiver_bp.route('/api/alerts/<patient_id>', methods=['GET'])
def get_alerts(patient_id):
    """Get alert history."""
    limit = request.args.get('limit', 50, type=int)
    severity = request.args.get('severity')
    result = caregiver_service.get_alerts(patient_id, limit, severity)
    return jsonify(result)


@caregiver_bp.route('/api/alerts/<alert_id>/read', methods=['POST'])
def mark_alert_read(alert_id):
    """Mark alert as read."""
    result = caregiver_service.mark_alert_read(alert_id)
    return jsonify(result)


@caregiver_bp.route('/api/device/battery/<patient_id>', methods=['GET'])
def get_battery(patient_id):
    """Get device battery status."""
    result = caregiver_service.get_device_battery(patient_id)
    return jsonify(result)


@caregiver_bp.route('/api/video/stream/<patient_id>', methods=['GET'])
def get_video_stream(patient_id):
    """Get video stream URL."""
    result = caregiver_service.get_live_video_stream_url(patient_id)
    return jsonify(result)

