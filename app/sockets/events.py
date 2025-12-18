"""
WebSocket Events for Real-time Dashboard Updates
"""
from flask_socketio import emit
from app import socketio


# Track connected clients
connected_clients = set()


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print(f"📡 Client connected")
    connected_clients.add(1)
    emit('connection_response', {
        'status': 'connected',
        'message': 'Connected to NovaCare Fall Detection System'
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print(f"📡 Client disconnected")
    if connected_clients:
        connected_clients.pop()


@socketio.on('subscribe_alerts')
def handle_subscribe_alerts():
    """Subscribe to real-time alert updates."""
    emit('subscribe_response', {
        'status': 'subscribed',
        'channel': 'alerts'
    })


@socketio.on('ping')
def handle_ping():
    """Handle ping for keep-alive."""
    emit('pong', {'timestamp': 'now'})


def broadcast_fall_alert(alert_data: dict):
    """
    Broadcast a fall alert to all connected clients.
    
    Args:
        alert_data: Dictionary containing alert information
    """
    socketio.emit('fall_alert', alert_data)
    print(f"🚨 Fall alert broadcasted to {len(connected_clients)} clients")


def broadcast_system_status(status_data: dict):
    """
    Broadcast system status update to all clients.
    
    Args:
        status_data: Dictionary containing system status
    """
    socketio.emit('system_status', status_data)


def broadcast_detection_update(detection_data: dict):
    """
    Broadcast detection update (for live monitoring).
    
    Args:
        detection_data: Dictionary containing detection result
    """
    socketio.emit('detection_update', detection_data)
