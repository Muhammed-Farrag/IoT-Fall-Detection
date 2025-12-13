"""
Emergency Service Dashboard Blueprint
Single Responsibility: Only handles HTTP routing for emergency dashboard
"""
from flask import Blueprint, render_template, jsonify, request
from app.services import EmergencyService

# Create blueprint
emergency_bp = Blueprint('emergency', __name__, url_prefix='/emergency')

# Dependency Injection
emergency_service = EmergencyService()


@emergency_bp.route('/')
@emergency_bp.route('/dashboard/<emergency_id>')
def dashboard(emergency_id=None):
    """Render the emergency dashboard."""
    return render_template('emergency/dashboard.html', emergency_id=emergency_id)


@emergency_bp.route('/api/emergency/<emergency_id>', methods=['GET'])
def get_emergency_details(emergency_id):
    """Get emergency details."""
    result = emergency_service.get_emergency_details(emergency_id)
    return jsonify(result)


@emergency_bp.route('/api/emergency/<emergency_id>/critical', methods=['GET'])
def get_critical_data(emergency_id):
    """Get critical data."""
    result = emergency_service.get_critical_data(emergency_id)
    return jsonify(result)


@emergency_bp.route('/api/emergency/<emergency_id>/status', methods=['POST'])
def update_status(emergency_id):
    """Update response status."""
    data = request.get_json()
    status = data.get('status')
    responder_id = data.get('responder_id')
    notes = data.get('notes')
    
    result = emergency_service.update_response_status(emergency_id, status, responder_id, notes)
    return jsonify(result)


@emergency_bp.route('/api/emergency/<emergency_id>/environmental', methods=['GET'])
def get_environmental_data(emergency_id):
    """Get environmental data."""
    result = emergency_service.get_environmental_data(emergency_id)
    return jsonify(result)


@emergency_bp.route('/api/emergency/<emergency_id>/audio-stream', methods=['GET'])
def get_audio_stream(emergency_id):
    """Get audio stream."""
    result = emergency_service.get_live_audio_stream(emergency_id)
    return jsonify(result)


@emergency_bp.route('/api/emergency/<emergency_id>/reassure', methods=['POST'])
def send_reassurance(emergency_id):
    """Send reassurance message."""
    data = request.get_json()
    message = data.get('message', 'Help is on the way. Stay calm.')
    result = emergency_service.send_reassurance_message(emergency_id, message)
    return jsonify(result)


@emergency_bp.route('/api/facilities', methods=['GET'])
def get_nearby_facilities():
    """Get nearby medical facilities."""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    result = emergency_service.get_nearby_facilities(lat, lng)
    return jsonify(result)

