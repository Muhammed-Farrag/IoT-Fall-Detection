"""
Health Professional Dashboard Blueprint
Single Responsibility: Only handles HTTP routing for health professional dashboard
"""
from flask import Blueprint, render_template, jsonify, request
from app.services import HealthProfessionalService

# Create blueprint
health_professional_bp = Blueprint('health_professional', __name__, url_prefix='/health-professional')

# Dependency Injection
health_service = HealthProfessionalService()


@health_professional_bp.route('/')
@health_professional_bp.route('/dashboard')
def dashboard():
    """Render the health professional dashboard."""
    return render_template('health_professional/dashboard.html')


@health_professional_bp.route('/api/patient/vitals/<patient_id>', methods=['GET'])
def get_vitals(patient_id):
    """Get current vitals."""
    result = health_service.get_current_vitals(patient_id)
    return jsonify(result)


@health_professional_bp.route('/api/patient/vitals/<patient_id>/history', methods=['GET'])
def get_vitals_history(patient_id):
    """Get vitals history."""
    vital_type = request.args.get('type')
    hours = request.args.get('hours', 24, type=int)
    result = health_service.get_vitals_history(patient_id, vital_type, hours)
    return jsonify(result)


@health_professional_bp.route('/api/patient/trends/<patient_id>', methods=['GET'])
def get_trends(patient_id):
    """Get health trends."""
    result = health_service.get_health_trends(patient_id)
    return jsonify(result)


@health_professional_bp.route('/api/patient/report/<patient_id>', methods=['POST'])
def generate_report(patient_id):
    """Generate health report."""
    data = request.get_json() or {}
    report_type = data.get('type', 'comprehensive')
    result = health_service.generate_health_report(patient_id, report_type)
    return jsonify(result)


@health_professional_bp.route('/api/patient/medication-adherence/<patient_id>', methods=['GET'])
def get_medication_adherence(patient_id):
    """Get medication adherence."""
    result = health_service.get_medication_adherence(patient_id)
    return jsonify(result)


@health_professional_bp.route('/api/patient/falls/<patient_id>', methods=['GET'])
def get_fall_incidents(patient_id):
    """Get fall incident history."""
    days = request.args.get('days', 30, type=int)
    result = health_service.get_fall_incidents(patient_id, days)
    return jsonify(result)

