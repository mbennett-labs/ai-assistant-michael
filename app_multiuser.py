from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sys
import os

sys.path.append('.')
from quantum_auth import QuantumAwareAuth

app = Flask(__name__)
app.secret_key = 'quantum-shield-labs-demo-key'

auth_system = QuantumAwareAuth()

def requires_auth(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return '''
    <html><head><title>Quantum Shield Labs</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
    <h1>Quantum Shield Labs</h1>
    <h2>AI Calendar Assistant</h2>
    <p>Multi-user system with quantum-aware security</p>
    <a href="/login" style="background: blue; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Login</a>
    <a href="/register" style="background: green; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-left: 10px;">Sign Up</a>
    </body></html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        auth_result = auth_system.authenticate_user(username, password)
        
        if auth_result['success']:
            session['user_id'] = auth_result['user_id']
            session['username'] = auth_result['username']
            session['security_tier'] = auth_result['security_tier']
            return redirect(url_for('dashboard'))
        else:
            return f'''
            <html><body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h2>Login Failed</h2>
            <p style="color: red;">{auth_result['message']}</p>
            <a href="/login">Try Again</a>
            </body></html>
            '''
    
    return '''
    <html><head><title>Login - Quantum Shield Labs</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
    <h1>Quantum Shield Labs Login</h1>
    <form method="POST" style="max-width: 300px; margin: 0 auto;">
        <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 10px; margin: 5px 0;"><br>
        <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 10px; margin: 5px 0;"><br>
        <button type="submit" style="background: blue; color: white; padding: 10px 20px; border: none; border-radius: 5px; width: 100%;">Login</button>
    </form>
    <p><a href="/register">Don't have an account? Sign up</a></p>
    </body></html>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        security_tier = request.form.get('security_tier', 'standard')
        
        reg_result = auth_system.register_user(username, email, password, security_tier)
        
        if reg_result['success']:
            return f'''
            <html><body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h2>Registration Successful!</h2>
            <p style="color: green;">{reg_result['message']}</p>
            <a href="/login">Login Now</a>
            </body></html>
            '''
        else:
            return f'''
            <html><body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h2>Registration Failed</h2>
            <p style="color: red;">{reg_result['message']}</p>
            <a href="/register">Try Again</a>
            </body></html>
            '''
    
    return '''
    <html><head><title>Sign Up - Quantum Shield Labs</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h1>Join Quantum Shield Labs</h1>
    <form method="POST" style="max-width: 400px; margin: 0 auto;">
        <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 10px; margin: 5px 0;"><br>
        <input type="email" name="email" placeholder="Email" required style="width: 100%; padding: 10px; margin: 5px 0;"><br>
        <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 10px; margin: 5px 0;"><br>
        <select name="security_tier" style="width: 100%; padding: 10px; margin: 5px 0;">
            <option value="standard">Standard Security (Free)</option>
            <option value="premium">Premium Quantum Shield ($9.99/month)</option>
        </select><br>
        <button type="submit" style="background: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; width: 100%;">Create Account</button>
    </form>
    <p><a href="/login">Already have an account? Login</a></p>
    </body></html>
    '''

@app.route('/dashboard')
@requires_auth
def dashboard():
    return f'''
    <html><head><title>Dashboard - Quantum Shield Labs</title></head>
    <body style="font-family: Arial; margin: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px;">
        <h1>Quantum Shield Labs Dashboard</h1>
        <p>Welcome back, {session['username']}!</p>
        <p>Security Level: {session['security_tier'].title()}</p>
    </div>
    <div style="margin-top: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2>AI Calendar Assistant</h2>
        <p>Your quantum-protected AI assistant is ready!</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Multi-user authentication</li>
            <li>Quantum-aware security</li>
            <li>Individual user sessions</li>
            <li>Ready for Google Calendar integration</li>
        </ul>
    </div>
    <p><a href="/logout" style="color: red;">Logout</a></p>
    </body></html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Starting Quantum Shield Labs Multi-User AI Calendar")
    print("Access at: http://localhost:5003")
    app.run(debug=True, port=5003)
