from flask import Flask, render_template
import os

# Get the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure Flask to use the app/templates and app/static folders
app = Flask(__name__, 
            template_folder=os.path.join(basedir, 'app', 'templates'),
            static_folder=os.path.join(basedir, 'app', 'static'))
app.secret_key = 'dev-secret-key-change-in-production'

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
