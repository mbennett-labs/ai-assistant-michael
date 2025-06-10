# Authentication wrapper to add to your existing AI Calendar Assistant
# This preserves ALL your existing AI functionality while adding multi-user login

from functools import wraps
from flask import session, redirect, url_for, request, flash, render_template_string
import sys
import os

# Add your quantum auth system
sys.path.append('.')
from quantum_auth_system import QuantumSecureAuth

# Initialize the quantum authentication system
quantum_auth = QuantumSecureAuth()

def requires_auth(f):
    """Decorator to protect routes with quantum-aware authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user has valid session
        session_token = session.get('session_token')
        if not session_token:
            return redirect(url_for('login'))
        
        # Verify session is still valid
        verification = quantum_auth.verify_session(session_token)
        if not verification['valid']:
            session.clear()
            flash('Session expired. Please login again.', 'warning')
            return redirect(url_for('login'))
        
        # Update session with current user info
        session['user_id'] = verification['user_id']
        session['username'] = verification['username']
        session['security_tier'] = verification['security_tier']
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current authenticated user information"""
    return {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'security_tier': session.get('security_tier', 'standard')
    }

# Login page template with quantum branding
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Shield Labs - AI Calendar Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #764ba2;
            font-size: 24px;
            margin-bottom: 5px;
        }
        .logo p {
            color: #666;
            font-size: 14px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .security-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        .security-info h4 {
            color: #333;
            margin-bottom: 8px;
        }
        .security-info ul {
            color: #666;
            font-size: 14px;
            margin-left: 20px;
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
        }
        .alert {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .alert-success {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>Quantum Shield Labs</h1>
            <p>AI Calendar Assistant - Secure Access</p>
        </div>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-error">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Access AI Calendar</button>
        </form>
        
        <div class="security-info">
            <h4>Quantum Security Features</h4>
            <ul>
                <li>Quantum-resistant password protection</li>
                <li>Encrypted personal data storage</li>
                <li>Secure session management</li>
            </ul>
        </div>
        
        <div class="links">
            <a href="/register">Create New Account</a>
        </div>
    </div>
</body>
</html>
'''

# Registration page template
REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Join Quantum Shield Labs</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .register-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 500px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #764ba2;
            font-size: 24px;
            margin-bottom: 5px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .security-tiers {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .tier {
            margin-bottom: 15px;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid transparent;
            cursor: pointer;
            transition: all 0.3s;
        }
        .tier:hover {
            border-color: #667eea;
        }
        .tier input[type="radio"] {
            width: auto;
            margin-right: 10px;
        }
        .tier-name {
            font-weight: 600;
            color: #333;
        }
        .tier-features {
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
        }
        .alert {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .alert-success {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
    </style>
</head>
<body>
    <div class="register-container">
        <div class="logo">
            <h1>Join Quantum Shield Labs</h1>
            <p>Create your secure AI Calendar account</p>
        </div>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-success">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="security-tiers">
                <h4>Choose Your Security Level</h4>
                <div class="tier">
                    <label>
                        <input type="radio" name="security_tier" value="standard" checked>
                        <span class="tier-name">Standard Security (Free)</span>
                        <div class="tier-features">
                            • Quantum-aware password protection<br>
                            • Encrypted data storage<br>
                            • Secure Google Calendar integration
                        </div>
                    </label>
                </div>
                <div class="tier">
                    <label>
                        <input type="radio" name="security_tier" value="premium">
                        <span class="tier-name">Premium Quantum Shield ($9.99/month)</span>
                        <div class="tier-features">
                            • All Standard features<br>
                            • NAORIS Protocol integration<br>
                            • Advanced threat detection<br>
                            • Priority support
                        </div>
                    </label>
                </div>
            </div>
            
            <button type="submit" class="btn">Create Quantum-Protected Account</button>
        </form>
        
        <div class="links">
            <a href="/login">Already have an account? Login</a>
        </div>
    </div>
</body>
</html>
'''

# Routes to add to your existing Flask app
def add_auth_routes(app):
    """Add authentication routes to your existing Flask app"""
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                flash('Please enter both username and password', 'error')
                return render_template_string(LOGIN_TEMPLATE)
            
            auth_result = quantum_auth.authenticate_user(username, password)
            
            if auth_result['success']:
                session['session_token'] = auth_result['session_token']
                session['user_id'] = auth_result['user_id']
                session['username'] = auth_result['username']
                session['security_tier'] = auth_result['security_tier']
                session.permanent = True
                
                flash(f"Welcome back! {auth_result['security_tier'].title()} security active", 'success')
                return redirect(url_for('home'))  # Redirect to your AI assistant
            else:
                flash(auth_result['message'], 'error')
        
        return render_template_string(LOGIN_TEMPLATE)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            security_tier = request.form.get('security_tier', 'standard')
            
            if not all([username, email, password]):
                flash('Please fill in all required fields', 'error')
                return render_template_string(REGISTER_TEMPLATE)
            
            reg_result = quantum_auth.register_user(username, email, password, security_tier)
            
            if reg_result['success']:
                flash(f"Account created successfully! {reg_result['message']}", 'success')
                return redirect(url_for('login'))
            else:
                flash(reg_result['message'], 'error')
        
        return render_template_string(REGISTER_TEMPLATE)
    
    @app.route('/logout')
    def logout():
        session_token = session.get('session_token')
        if session_token:
            quantum_auth.logout_user(session_token)
        
        session.clear()
        flash('You have been securely logged out', 'success')
        return redirect(url_for('login'))

if __name__ == "__main__":
    print("Authentication wrapper ready!")
    print("Features:")
    print("- Multi-user login system")
    print("- Quantum security branding")
    print("- Session management")
    print("- Ready to integrate with your AI assistant")
