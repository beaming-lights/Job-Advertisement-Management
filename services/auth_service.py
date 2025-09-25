"""
Authentication Service for User Session Management
Enhanced to work with real API authentication
Handles login, logout, session state, and role-based access control
"""

import os
import json
import hashlib
import secrets
import requests
from typing import Dict, Optional, Literal
from datetime import datetime, timedelta
from nicegui import app, ui

UserRole = Literal['vendor', 'user', 'job_seeker', 'employer', 'admin']

class AuthService:
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', 'https://advertisement-management-api-91xh.onrender.com').rstrip('/')
        self.sessions = {}  # Keep for backward compatibility
        self.users = {}     # Keep for fallback
        self.session_timeout = timedelta(hours=24)
        self._storage_warned = False
        self.current_user = None
        self.access_token = None
        self._load_users()  # Load local users as fallback
    
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
        """Register a new user using API or fallback to local"""
        # Try API registration first
        if self.base_url:
            try:
                data = {
                    "email": email,
                    "password": password,
                    "full_name": name,
                    "role": role,
                    "is_active": True
                }
                
                response = requests.post(
                    f"{self.base_url}/users/register",
                    json=data,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    return {"success": True, "message": "Registration successful! Please login."}
                elif response.status_code == 400:
                    return {"success": False, "message": "Email already exists or invalid data"}
                else:
                    print(f"API registration failed: {response.status_code}")
                    # Fall through to local registration
                    
            except Exception as e:
                print(f"API registration error: {e}")
                # Fall through to local registration
        
        # Fallback to local registration
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
        """Authenticate user using API or fallback to local"""
        # Try API login first
        if self.base_url:
            try:
                # API expects both username and email fields for login
                # Generate username from email (same logic as registration)
                username = email.split('@')[0] if email else ""
                
                data = {
                    "username": username,
                    "email": email,
                    "password": password
                }
                
                response = requests.post(
                    f"{self.base_url}/users/login",
                    data=data,  # Send as form data instead of JSON
                    timeout=10
                )
                
                if response.status_code == 200:
                    login_data = response.json()
                    
                    # Extract token from API response
                    self.access_token = login_data.get("access_token")
                    
                    # Get stored user info for role mapping
                    stored_user = self.users.get(email, {})
                    user_role = stored_user.get("role", "job_seeker")  # Default to job_seeker
                    user_name = stored_user.get("name", username)
                    
                    self.current_user = {
                        "email": email,
                        "name": user_name,
                        "role": user_role,
                        "username": username,
                        "is_active": True,
                        "api_authenticated": True
                    }
                    
                    # Store in app storage
                    try:
                        app.storage.user['access_token'] = self.access_token
                        app.storage.user['user_data'] = self.current_user
                        app.storage.user['login_time'] = datetime.now().isoformat()
                        app.storage.user['auth_method'] = 'api'
                    except RuntimeError as e:
                        if "storage_secret" in str(e):
                            self._warn_storage_once()
                    
                    return {
                        "success": True,
                        "message": "Login successful",
                        "user": self.current_user,
                        "token": self.access_token
                    }
                else:
                    print(f"API login failed: {response.status_code}")
                    # Fall through to local login
                    
            except Exception as e:
                print(f"API login error: {e}")
                # Fall through to local login
        
        # Fallback to local authentication
        if email not in self.users:
            return {"success": False, "message": "Invalid email or password"}
        
        user = self.users[email]
        if not self._verify_password(password, user["password_hash"]):
            return {"success": False, "message": "Invalid email or password"}
        
        # Create local session
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "email": email,
            "role": user["role"],
            "name": user["name"],
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        
        self.current_user = {
            "email": email,
            "role": user["role"],
            "name": user["name"]
        }
        
        # Store session in app storage
        try:
            app.storage.user['session_id'] = session_id
            app.storage.user['user_data'] = self.current_user
            app.storage.user['auth_method'] = 'local'
        except RuntimeError as e:
            if "storage_secret" in str(e):
                self._warn_storage_once()
        
        return {
            "success": True, 
            "message": "Login successful",
            "user": self.current_user
        }
    
    def logout(self):
        """Clear user session and API token"""
        # Clear current user and token
        self.current_user = None
        self.access_token = None
        
        # Clear app storage
        try:
            if 'session_id' in app.storage.user:
                session_id = app.storage.user['session_id']
                # Remove session from memory
                if session_id in self.sessions:
                    del self.sessions[session_id]
            
            # Clear all user storage
            app.storage.user.clear()
        except RuntimeError as e:
            if "storage_secret" in str(e):
                self._warn_storage_once()
            else:
                raise e
    
    def get_current_user(self) -> Optional[Dict]:
        """Get currently logged in user"""
        # Return in-memory user if available
        if self.current_user:
            return self.current_user
            
        # Try to restore from app storage
        try:
            if 'user_data' in app.storage.user:
                user_data = app.storage.user['user_data']
                self.current_user = user_data
                
                # Also restore token if available
                if 'access_token' in app.storage.user:
                    self.access_token = app.storage.user['access_token']
                
                return user_data
        except RuntimeError as e:
            if "storage_secret" in str(e):
                self._warn_storage_once()
            else:
                raise e
        return None
    
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
    
    def get_authenticated_headers(self) -> Dict[str, str]:
        """Get headers for API requests with authentication"""
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Add Bearer token if available
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        # Add user info for tracking if available
        user = self.get_current_user()
        if user:
            headers['X-User-Email'] = user.get('email', '')
            headers['X-User-Role'] = user.get('role', '')
        
        return headers
    
    def api_register_user(self, email: str, password: str, name: str, role: str = "job_seeker") -> Dict:
        """Register user using API only (no local fallback)"""
        if not self.base_url:
            return {"success": False, "message": "API service not available"}
            
        try:
            # Map role to API expectations
            role_mapping = {
                "vendor": "employer",
                "employer": "employer", 
                "job_seeker": "candidate",
                "user": "candidate",
                "admin": "admin"
            }
            api_role = role_mapping.get(role, "candidate")  # Default to candidate
            
            # Create username from email (before @ symbol) if not provided separately
            username = email.split('@')[0] if email else name.lower().replace(' ', '_')
            
            data = {
                "username": username,
                "email": email,
                "password": password,
                "full_name": name,
                "role": api_role
            }
            
            response = requests.post(
                f"{self.base_url}/users/register",
                data=data,  # Send as form data instead of JSON
                timeout=10
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Store user info locally for login role mapping
                user_info = {
                    "username": username,
                    "role": role,  # Store the original role, not the API role
                    "name": name,
                    "created_at": datetime.now().isoformat(),
                    "api_registered": True
                }
                self.users[email] = user_info
                self._save_users()
                
                return {
                    "success": True,
                    "message": response_data.get("message", "Registration successful! Please login with your credentials."),
                    "user": {
                        "username": username,
                        "email": email,
                        "name": name,
                        "role": role  # Return the role as expected by the app
                    }
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                raw_detail = error_data.get("detail", f"Registration failed (HTTP {response.status_code})")
                
                # Handle case where detail might be a list or other non-string type
                if isinstance(raw_detail, list):
                    error_message = "; ".join(str(item) for item in raw_detail)
                else:
                    error_message = str(raw_detail)
                    
                return {"success": False, "message": error_message}
                
        except requests.exceptions.Timeout:
            return {"success": False, "message": "Registration request timed out. Please try again."}
        except requests.exceptions.ConnectionError:
            return {"success": False, "message": "Unable to connect to registration service. Please check your internet connection."}
        except Exception as e:
            return {"success": False, "message": f"Registration error: {str(e)}"}

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
