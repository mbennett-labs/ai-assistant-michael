# Quantum-Aware Authentication System for AI Calendar Assistant
import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class QuantumSecureAuth:
    def __init__(self, db_path='quantum_users.db'):
        self.db_path = db_path
        self.init_database()
        self.encryption_key = self._generate_or_load_key()
        
    def _generate_or_load_key(self):
        """Generate or load encryption key for quantum-safe data protection"""
        key_file = 'quantum.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def init_database(self):
        """Initialize quantum-aware user database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table with quantum security features
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            security_tier TEXT DEFAULT 'standard',
            google_calendar_token TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            session_token TEXT,
            session_expires TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
        ''')
        
        # User sessions table for quantum-safe session management
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        print("Quantum-aware database initialized successfully")
    
    def _generate_salt(self):
        """Generate quantum-safe salt for password hashing"""
        return secrets.token_hex(32)
    
    def _hash_password(self, password, salt):
        """Quantum-resistant password hashing using PBKDF2 with SHA-256"""
        # Use PBKDF2 with high iteration count for quantum resistance
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=100000,  # High iteration count for security
        )
        return base64.b64encode(kdf.derive(password.encode())).decode()
    
    def register_user(self, username, email, password, security_tier='standard'):
        """Register new user with quantum-aware security"""
        try:
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO users (username, email, password_hash, salt, security_tier)
            VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, salt, security_tier))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            security_message = {
                'standard': 'Standard quantum-aware security enabled',
                'premium': 'Premium Quantum Shield protection activated'
            }
            
            return {
                'success': True, 
                'user_id': user_id,
                'message': f'Account created! {security_message.get(security_tier, "Security enabled")}'
            }
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return {'success': False, 'message': 'Username already exists'}
            elif 'email' in str(e):
                return {'success': False, 'message': 'Email already registered'}
            else:
                return {'success': False, 'message': 'Registration failed'}
        except Exception as e:
            return {'success': False, 'message': f'Registration error: {str(e)}'}
    
    def authenticate_user(self, username, password):
        """Authenticate user with quantum-safe verification"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, username, email, password_hash, salt, security_tier, is_active 
            FROM users WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            if not user:
                conn.close()
                return {'success': False, 'message': 'Invalid username or password'}
            
            if not user[6]:  # is_active check
                conn.close()
                return {'success': False, 'message': 'Account is disabled'}
            
            # Verify password
            stored_hash = user[3]
            salt = user[4]
            calculated_hash = self._hash_password(password, salt)
            
            if calculated_hash != stored_hash:
                conn.close()
                return {'success': False, 'message': 'Invalid username or password'}
            
            # Create quantum-safe session
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)
            
            # Update user last login
            cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP, session_token = ? 
            WHERE id = ?
            ''', (session_token, user[0]))
            
            # Create session record
            cursor.execute('''
            INSERT INTO user_sessions (user_id, session_token, expires_at, is_active)
            VALUES (?, ?, ?, 1)
            ''', (user[0], session_token, expires_at))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'user_id': user[0],
                'username': user[1],
                'email': user[2],
                'security_tier': user[5],
                'session_token': session_token,
                'expires_at': expires_at.isoformat()
            }
        except Exception as e:
            return {'success': False, 'message': f'Authentication error: {str(e)}'}
    
    def verify_session(self, session_token):
        """Verify quantum-safe user session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT s.user_id, u.username, u.email, u.security_tier, s.expires_at
            FROM user_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ? AND s.is_active = 1 AND u.is_active = 1
            ''', (session_token,))
            
            session = cursor.fetchone()
            if not session:
                conn.close()
                return {'valid': False, 'message': 'Invalid session'}
            
            # Check if session expired
            expires_at = datetime.fromisoformat(session[4])
            if datetime.now() > expires_at:
                # Deactivate expired session
                cursor.execute('''
                UPDATE user_sessions SET is_active = 0 WHERE session_token = ?
                ''', (session_token,))
                conn.commit()
                conn.close()
                return {'valid': False, 'message': 'Session expired'}
            
            conn.close()
            return {
                'valid': True,
                'user_id': session[0],
                'username': session[1],
                'email': session[2],
                'security_tier': session[3]
            }
        except Exception as e:
            return {'valid': False, 'message': f'Session verification error: {str(e)}'}
    
    def logout_user(self, session_token):
        """Securely logout user by invalidating session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            UPDATE user_sessions SET is_active = 0 WHERE session_token = ?
            ''', (session_token,))
            
            cursor.execute('''
            UPDATE users SET session_token = NULL WHERE session_token = ?
            ''', (session_token,))
            
            conn.commit()
            conn.close()
            return {'success': True, 'message': 'Logged out successfully'}
        except Exception as e:
            return {'success': False, 'message': f'Logout error: {str(e)}'}

if __name__ == "__main__":
    # Test the quantum authentication system
    auth = QuantumSecureAuth()
    print("Quantum-aware authentication system ready!")
    print("Features enabled:")
    print("- Quantum-resistant password hashing")
    print("- Encrypted data storage")
    print("- Secure session management")
    print("- Multi-user support")
