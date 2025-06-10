# Quantum Authentication - Local Version
import sqlite3
import hashlib
import secrets
from datetime import datetime

class QuantumAwareAuth:
    def __init__(self, db_path='quantum_users.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            security_tier TEXT DEFAULT 'standard',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_token TEXT
        )
        ''')
        conn.commit()
        conn.close()
        print("Quantum database ready")
    
    def register_user(self, username, email, password, security_tier='standard'):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO users (username, email, password_hash, security_tier)
            VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, security_tier))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': f'User registered with {security_tier} security'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def authenticate_user(self, username, password):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, username, email, security_tier FROM users 
            WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            if user:
                session_token = secrets.token_hex(32)
                cursor.execute('UPDATE users SET session_token = ? WHERE id = ?', 
                              (session_token, user[0]))
                conn.commit()
                conn.close()
                
                return {
                    'success': True,
                    'user_id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'security_tier': user[3],
                    'session_token': session_token
                }
            else:
                conn.close()
                return {'success': False, 'message': 'Invalid credentials'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
