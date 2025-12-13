"""
Main application entry point
Run this file to start the Flask development server
"""
import os
from app import create_app

# Get configuration from environment or use default
config_name = os.environ.get('FLASK_CONFIG') or 'development'
app = create_app()

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print(f"🤖 NovaBot Application Starting...")
    print("="*60)
    print(f"Environment: {config_name}")
    print(f"Running on: http://127.0.0.1:{port}")
    print("\nAvailable Dashboards:")
    print("  • Primary User:        http://127.0.0.1:{}/primary".format(port))
    print("  • Caregiver:           http://127.0.0.1:{}/caregiver".format(port))
    print("  • Health Professional: http://127.0.0.1:{}/health-professional".format(port))
    print("  • Emergency Service:   http://127.0.0.1:{}/emergency".format(port))
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
