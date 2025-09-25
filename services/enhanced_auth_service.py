"""
Enhanced Authentication Service with API Integration
Integrates with the Job Hub API for real authentication
"""

import os
import requests
from typing import Dict, Optional, Literal
from datetime import datetime, timedelta
from nicegui import app, ui

UserRole = Literal['vendor', 'job_seeker', 'admin']

class EnhancedAuthService:
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', '').rstrip('/')
        self.current_user = None
        self.access_token = None
        self.token_expiry = None
        
    def _make_request(self, method: str, endpoint: str, data: Dict = None, auth_required: bool = False) -> Dict:
        """Make authenticated API request"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if auth_required and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        try:
            if method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            else:
                return {"success": False, "message": f"Unsupported method: {method}"}
                
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            elif response.status_code == 401:
                return {"success": False, "message": "Authentication failed"}
            elif response.status_code == 403:
                return {"success": False, "message": "Access forbidden"}
            else:
                return {"success": False, "message": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "message": f"Request failed: {str(e)}"}
    
    def register_user(self, email: str, password: str, full_name: str, role: UserRole = 'job_seeker') -> Dict:
        """Register new user with API"""
        data = {
            "email": email,
            "password": password,
            "full_name": full_name,
            "role": role,
            "is_active": True
        }
        
        result = self._make_request('POST', '/users/register', data)
        
        if result["success"]:
            return {"success": True, "message": "Registration successful! Please login."}
        else:
            return {"success": False, "message": result["message"]}
    
    def login(self, email: str, password: str) -> Dict:
        """Login user with API"""
        data = {
            "username": email,  # API might expect 'username' field
            "password": password
        }
        
        result = self._make_request('POST', '/users/login', data)
        
        if result["success"]:
            login_data = result["data"]
            
            # Extract token and user info from API response
            self.access_token = login_data.get("access_token")
            user_info = login_data.get("user", {})
            
            self.current_user = {
                "id": user_info.get("id"),
                "email": user_info.get("email", email),
                "full_name": user_info.get("full_name", ""),
                "role": user_info.get("role", "job_seeker"),
                "is_active": user_info.get("is_active", True)
            }
            
            # Store in app storage for persistence
            try:
                app.storage.user['access_token'] = self.access_token
                app.storage.user['user_data'] = self.current_user
                app.storage.user['login_time'] = datetime.now().isoformat()
            except RuntimeError:
                pass  # Storage not available
            
            return {
                "success": True,
                "message": "Login successful",
                "user": self.current_user,
                "token": self.access_token
            }
        else:
            return {"success": False, "message": result["message"]}
    
    def logout(self):
        """Logout user and clear session"""
        self.current_user = None
        self.access_token = None
        self.token_expiry = None
        
        try:
            app.storage.user.clear()
        except RuntimeError:
            pass
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user"""
        if self.current_user:
            return self.current_user
            
        # Try to restore from storage
        try:
            stored_token = app.storage.user.get('access_token')
            stored_user = app.storage.user.get('user_data')
            login_time = app.storage.user.get('login_time')
            
            if stored_token and stored_user and login_time:
                # Check if token is still valid (24 hour expiry)
                login_dt = datetime.fromisoformat(login_time)
                if datetime.now() - login_dt < timedelta(hours=24):
                    self.access_token = stored_token
                    self.current_user = stored_user
                    return self.current_user
                else:
                    # Token expired, clear storage
                    self.logout()
        except RuntimeError:
            pass
            
        return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.get_current_user() is not None
    
    def is_vendor(self) -> bool:
        """Check if current user is a vendor/employer"""
        user = self.get_current_user()
        return user is not None and user.get("role") in ["vendor", "employer", "admin"]
    
    def is_job_seeker(self) -> bool:
        """Check if current user is a job seeker"""
        user = self.get_current_user()
        return user is not None and user.get("role") == "job_seeker"
    
    def require_auth(self, redirect_to: str = "/login") -> bool:
        """Require authentication"""
        if not self.is_authenticated():
            ui.navigate.to(redirect_to)
            return False
        return True
    
    def require_vendor(self, redirect_to: str = "/login") -> bool:
        """Require vendor role"""
        if not self.is_vendor():
            ui.navigate.to(redirect_to)
            return False
        return True
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get headers for authenticated API requests"""
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}
    
    def update_profile(self, profile_data: Dict) -> Dict:
        """Update user profile (placeholder - implement based on API)"""
        # This would need a PUT /users/{user_id} endpoint
        return {"success": False, "message": "Profile update not implemented in API"}
    
    def change_password(self, old_password: str, new_password: str) -> Dict:
        """Change user password (placeholder - implement based on API)"""
        # This would need a PUT/POST endpoint for password change
        return {"success": False, "message": "Password change not implemented in API"}

# Global enhanced auth service
enhanced_auth_service = EnhancedAuthService()