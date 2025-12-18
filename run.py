"""
NovaCare Fall Detection System
Main Application Entry Point
"""
from flask import render_template
import os
import atexit
import webbrowser
import threading

# Get the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Import app factory
from app import create_app, socketio, db

# Create application
app = create_app()

# Import processor after app is created
from app.processor import create_processor

# Global processor reference
processor = None


# ===================================
# TEMPLATE ROUTES
# ===================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/alerts')
def alerts():
    return render_template('alerts.html')


@app.route('/health')
def health():
    return render_template('health.html')


# ===================================
# STARTUP & SHUTDOWN
# ===================================

def start_detection():
    """Start the detection processor."""
    global processor
    processor = create_processor(app, db)
    processor.start()


def shutdown_detection():
    """Stop the detection processor on shutdown."""
    global processor
    if processor:
        processor.stop()


def open_browser():
    """Open browser after short delay to allow server to start."""
    import time
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open('http://localhost:5000/dashboard')


# Register shutdown handler
atexit.register(shutdown_detection)


# ===================================
# MAIN ENTRY
# ===================================

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     🏥 NovaCare Fall Detection System                     ║
    ║     ──────────────────────────────────────────────────    ║
    ║     Starting server with AI-powered fall detection...    ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Open browser automatically
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start detection processor in background
    socketio.start_background_task(start_detection)
    
    print("🌐 Opening browser at: http://localhost:5000/dashboard")
    print("📹 Live stream will connect to Raspberry Pi camera")
    print("\n   Press Ctrl+C to stop the server\n")
    
    # Run with SocketIO
    socketio.run(
        app, 
        debug=False,  # Disable debug to prevent double start
        host='0.0.0.0', 
        port=5000,
        use_reloader=False
    )
