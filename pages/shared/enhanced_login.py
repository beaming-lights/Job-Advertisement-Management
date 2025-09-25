"""
Enhanced Login Page with Real API Integration
"""

from nicegui import ui
from services.enhanced_auth_service import enhanced_auth_service

def enhanced_login_page():
    """Enhanced login page with real API integration"""
    
    # State
    email = ""
    password = ""
    loading = False
    
    # Add modern styling
    ui.add_head_html("""
    <style>
    .auth-container {
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .auth-card {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 400px;
    }
    .auth-input {
        margin-bottom: 1rem;
    }
    .auth-button {
        width: 100%;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .auth-link {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    .auth-link:hover {
        text-decoration: underline;
    }
    </style>
    """)
    
    with ui.element('div').classes('auth-container'):
        with ui.element('div').classes('auth-card'):
            # Header
            with ui.column().classes('items-center mb-8'):
                ui.icon('work', size='3rem').classes('text-blue-600 mb-4')
                ui.label('Welcome Back').classes('text-2xl font-bold text-gray-800')
                ui.label('Sign in to your account').classes('text-gray-600')
            
            # Form
            with ui.column().classes('w-full space-y-4'):
                email_input = ui.input('Email', placeholder='Enter your email')\
                    .classes('auth-input w-full').props('outlined')
                    
                password_input = ui.input('Password', placeholder='Enter your password', password=True)\
                    .classes('auth-input w-full').props('outlined')
                
                # Remember me checkbox
                remember_me = ui.checkbox('Remember me').classes('text-sm text-gray-600')
                
                # Login button
                login_btn = ui.button('Sign In', on_click=lambda: handle_login())\
                    .classes('auth-button').props('color=primary')
                
                # Loading indicator
                loading_indicator = ui.spinner().classes('hidden')
                
                # Error message
                error_label = ui.label('').classes('text-red-500 text-sm hidden')
                
                # Divider
                with ui.row().classes('w-full items-center my-6'):
                    ui.separator().classes('flex-1')
                    ui.label('or').classes('text-gray-400 px-4')
                    ui.separator().classes('flex-1')
                
                # Register link
                with ui.row().classes('justify-center'):
                    ui.label("Don't have an account?").classes('text-gray-600')
                    ui.link('Sign up', '/register').classes('auth-link ml-1')
    
    async def handle_login():
        nonlocal loading
        
        if loading:
            return
            
        email_val = email_input.value or ""
        password_val = password_input.value or ""
        
        # Validation
        if not email_val or not password_val:
            show_error("Please fill in all fields")
            return
        
        # Show loading
        loading = True
        login_btn.props('loading')
        loading_indicator.classes(remove='hidden')
        error_label.classes(add='hidden')
        
        try:
            # Attempt login
            result = enhanced_auth_service.login(email_val, password_val)
            
            if result["success"]:
                ui.notify("Login successful!", type="positive")
                
                # Redirect based on user role
                user = result["user"]
                if user.get("role") in ["vendor", "employer", "admin"]:
                    ui.navigate.to("/vendor-dashboard")
                else:
                    ui.navigate.to("/job-seeker-dashboard")
            else:
                show_error(result["message"])
        
        except Exception as e:
            show_error(f"Login failed: {str(e)}")
        
        finally:
            loading = False
            login_btn.props(remove='loading')
            loading_indicator.classes(add='hidden')
    
    def show_error(message: str):
        error_label.text = message
        error_label.classes(remove='hidden')
        ui.notify(message, type="negative")

# For backward compatibility
def login_page():
    """Backward compatible login page"""
    return enhanced_login_page()