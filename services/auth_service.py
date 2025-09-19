"""
Authentication Service for User Session Management
Handles login, logout, session state, and role-based access control
"""

import os
import json
import hashlib
import secrets
from typing import Dict, Optional, Literal
from datetime import datetime, timedelta
from nicegui import app, ui

UserRole = Literal['vendor', 'user']

class AuthService:
    def __init__(self):
        self.sessions = {}  # In production, use Redis or database
        self.users = {}     # In production, use database
        self.session_timeout = timedelta(hours=24)
        self._storage_warned = False  # ensure we only warn once about storage_secret
        self._load_users()
    
    def _load_users(self):
        """Load users from file (in production, use database)"""
        users_file = "users.json"
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            # Create default admin user for testing
            self.users = {
                "admin@test.com": {
                    "password_hash": self._hash_password("admin123"),
                    "role": "vendor",
                    "name": "Admin User",
                    "created_at": datetime.now().isoformat()
                }
            }
            self._save_users()
    
    def _save_users(self):
        """Save users to file (in production, use database)"""
        try:
            with open("users.json", 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _warn_storage_once(self):
        """Warn once (and only in DEBUG) if storage_secret is missing"""
        if not self._storage_warned:
            debug = os.getenv('DEBUG', 'True').lower() == 'true'
            if debug:
                print("Warning: app.storage.user requires storage_secret in ui.run(). Session will not persist.")
            self._storage_warned = True
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_hex = password_hash.split(':')
            password_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_check.hex() == hash_hex
        except:
            return False
    
    def register_user(self, email: str, password: str, name: str, role: UserRole) -> Dict:
        """Register a new user"""
        if email in self.users:
            return {"success": False, "message": "Email already exists"}
        
        if len(password) < 6:
            return {"success": False, "message": "Password must be at least 6 characters"}
        
        self.users[email] = {
            "password_hash": self._hash_password(password),
            "role": role,
            "name": name,
            "created_at": datetime.now().isoformat()
        }
        
        self._save_users()
        return {"success": True, "message": "User registered successfully"}
    
    def login(self, email: str, password: str) -> Dict:
        """Authenticate user and create session"""
        if email not in self.users:
            return {"success": False, "message": "Invalid email or password"}
        
        user = self.users[email]
        if not self._verify_password(password, user["password_hash"]):
            return {"success": False, "message": "Invalid email or password"}
        
        # Create session
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "email": email,
            "role": user["role"],
            "name": user["name"],
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        
        # Store session in app storage
        try:
            app.storage.user['session_id'] = session_id
            app.storage.user['user_data'] = {
                "email": email,
                "role": user["role"],
                "name": user["name"]
            }
        except RuntimeError as e:
            if "storage_secret" in str(e):
                self._warn_storage_once()
                # Fallback to in-memory session only
            else:
                raise e
        
        return {
            "success": True, 
            "message": "Login successful",
            "user": {
                "email": email,
                "role": user["role"],
                "name": user["name"]
            }
        }
    
    def logout(self):
        """Logout user and clear session"""
        try:
            session_id = app.storage.user.get('session_id')
            if session_id and session_id in self.sessions:
                del self.sessions[session_id]
            
            # Clear app storage
            app.storage.user.clear()
        except RuntimeError as e:
            if "storage_secret" in str(e):
                self._warn_storage_once()
                # Clear all sessions as fallback
                self.sessions.clear()
            else:
                raise e
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user"""
        try:
            session_id = app.storage.user.get('session_id')
        except RuntimeError as e:
            if "storage_secret" in str(e):
                # Fallback: no persistent sessions, return None
                return None
            else:
                raise e
                
        if not session_id or session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check session timeout
        if datetime.now() - session['last_activity'] > self.session_timeout:
            self.logout()
            return None
        
        # Update last activity
        session['last_activity'] = datetime.now()
        
        return {
            "email": session["email"],
            "role": session["role"],
            "name": session["name"]
        }
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.get_current_user() is not None
    
    def is_vendor(self) -> bool:
        """Check if current user is a vendor"""
        user = self.get_current_user()
        return user is not None and user["role"] == "vendor"
    
    def is_user(self) -> bool:
        """Check if current user is a regular user"""
        user = self.get_current_user()
        return user is not None and user["role"] == "user"
    
    def require_auth(self, redirect_to: str = "/login"):
        """Decorator/middleware to require authentication"""
        if not self.is_authenticated():
            ui.navigate.to(redirect_to)
            return False
        return True
    
    def require_vendor(self, redirect_to: str = "/login"):
        """Decorator/middleware to require vendor role"""
        if not self.is_vendor():
            ui.navigate.to(redirect_to)
            return False
        return True
    
    def get_user_stats(self, email: str) -> Dict:
        """Get user statistics (for vendor dashboard)"""
        # This would typically query the database for user-specific stats
        # For now, return mock data
        return {
            "total_ads": 0,
            "active_ads": 0,
            "views": 0,
            "applications": 0
        }

# Global auth service instance
auth_service = AuthService()
