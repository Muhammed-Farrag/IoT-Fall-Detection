"""
Primary User Dashboard Blueprint - Routes for primary user interface
Single Responsibility: Only handles HTTP routing for primary user dashboard
"""
from flask import Blueprint, render_template, jsonify, request
from app.services import CommunicationService, HealthService, NavigationService, SettingsService
from app.models import InputMode, NotificationType, FollowMode, AccessibilityMode, DataSharingLevel

# Create blueprint
primary_bp = Blueprint('primary', __name__, url_prefix='/primary')

# Dependency Injection: Initialize services
communication_service = CommunicationService()
health_service = HealthService(communication_service)
navigation_service = NavigationService()
settings_service = SettingsService()


# ============================================================================
# VIEW ROUTES (Render HTML)
# ============================================================================

@primary_bp.route('/')
@primary_bp.route('/dashboard')
def dashboard():
    """Render the primary user dashboard."""
    return render_template('primary_user/dashboard.html')


# ============================================================================
# API ROUTES (Business Logic via Services)
# ============================================================================

# Communication Hub Endpoints

@primary_bp.route('/api/input-mode', methods=['GET'])
def get_input_mode():
    """Get the current active input mode."""
    mode = communication_service.get_active_mode()
    return jsonify({
        'success': True,
        'active_mode': mode.value
    })


@primary_bp.route('/api/input-mode', methods=['POST'])
def set_input_mode():
    """Set the active input mode."""
    data = request.get_json()
    mode_str = data.get('mode')
    
    try:
        mode = InputMode(mode_str)
        result = communication_service.set_active_mode(mode)
        return jsonify(result)
    except ValueError:
        return jsonify({
            'success': False,
            'message': f'Invalid input mode: {mode_str}'
        }), 400


@primary_bp.route('/api/visual-feedback', methods=['GET'])
def get_visual_feedback():
    """Get visual feedback queue."""
    queue = communication_service.get_visual_feedback_queue()
    return jsonify({
        'success': True,
        'feedback': queue
    })


@primary_bp.route('/api/visual-feedback', methods=['POST'])
def send_visual_feedback():
    """Send visual feedback."""
    data = request.get_json()
    text = data.get('text', '')
    duration = data.get('duration', 5)
    
    result = communication_service.send_visual_feedback(text, duration)
    return jsonify(result)


# Health & Wellness Endpoints

@primary_bp.route('/api/medication/next', methods=['GET'])
def get_next_medication():
    """Get the next scheduled medication."""
    user_id = request.args.get('user_id', 'default_user')
    result = health_service.get_next_medication(user_id)
    return jsonify(result)


@primary_bp.route('/api/medication/schedules', methods=['GET'])
def get_medication_schedules():
    """Get all medication schedules."""
    user_id = request.args.get('user_id', 'default_user')
    result = health_service.get_schedules(user_id)
    return jsonify(result)


@primary_bp.route('/api/medical-query', methods=['POST'])
def medical_query():
    """Query the medical knowledge base (RAG)."""
    data = request.get_json()
    question = data.get('question', '')
    context = data.get('context', {})
    
    if not question:
        return jsonify({
            'success': False,
            'message': 'Question is required'
        }), 400
    
    result = health_service.query(question, context)
    return jsonify(result)


# Navigation & Vision Endpoints

@primary_bp.route('/api/navigation/follow-mode', methods=['GET'])
def get_follow_mode():
    """Get follow mode status."""
    status = navigation_service.get_follow_status()
    return jsonify({
        'success': True,
        'status': status
    })


@primary_bp.route('/api/navigation/follow-mode', methods=['POST'])
def toggle_follow_mode():
    """Toggle follow mode."""
    data = request.get_json()
    activate = data.get('activate', False)
    person_id = data.get('person_id')
    
    result = navigation_service.toggle_follow_mode(activate, person_id)
    return jsonify(result)


@primary_bp.route('/api/vision/identify', methods=['POST'])
def identify_object():
    """Identify objects in image."""
    # In real implementation, would handle image upload
    image_data = request.data or b''
    result = navigation_service.identify_object(image_data)
    return jsonify(result)


@primary_bp.route('/api/vision/read-text', methods=['POST'])
def read_text():
    """Read text from image (OCR)."""
    image_data = request.data or b''
    result = navigation_service.read_text(image_data)
    return jsonify(result)


@primary_bp.route('/api/vision/describe-scene', methods=['POST'])
def describe_scene():
    """Describe the scene in natural language."""
    image_data = request.data or b''
    result = navigation_service.describe_scene(image_data)
    return jsonify(result)


# Settings & Privacy Endpoints

@primary_bp.route('/api/settings', methods=['GET'])
def get_settings():
    """Get all user settings."""
    user_id = request.args.get('user_id', 'default_user')
    result = settings_service.get_all_settings(user_id)
    return jsonify(result)


@primary_bp.route('/api/settings/accessibility', methods=['POST'])
def update_accessibility():
    """Update accessibility settings."""
    data = request.get_json()
    user_id = data.get('user_id', 'default_user')
    mode_str = data.get('mode')
    
    try:
        mode = AccessibilityMode(mode_str)
        result = settings_service.update_accessibility_mode(user_id, mode)
        return jsonify(result)
    except ValueError:
        return jsonify({
            'success': False,
            'message': f'Invalid accessibility mode: {mode_str}'
        }), 400


@primary_bp.route('/api/settings/privacy', methods=['POST'])
def update_privacy():
    """Update privacy settings."""
    data = request.get_json()
    user_id = data.get('user_id', 'default_user')
    sharing_level_str = data.get('sharing_level')
    
    try:
        sharing_level = DataSharingLevel(sharing_level_str)
        result = settings_service.update_data_sharing(user_id, sharing_level)
        return jsonify(result)
    except ValueError:
        return jsonify({
            'success': False,
            'message': f'Invalid sharing level: {sharing_level_str}'
        }), 400

