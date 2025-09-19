"""
Login Page - Authentication for Vendors and Users
"""

from nicegui import ui
from services.auth_service import auth_service
from components.header import create_header
from components.footer import create_footer

@ui.page("/login")
def login_page():
    """Create the login page"""
    
    # Check if already authenticated
    if auth_service.is_authenticated():
        current_user = auth_service.get_current_user()
        if current_user["role"] == "vendor":
            ui.navigate.to("/vendor-dashboard")
        else:
            ui.navigate.to("/job-seeker-dashboard")
        return
    
    # Add CSS for styling
    ui.add_head_html("""
        <style>
        body {
            overflow-x: hidden !important;
        }
        .nicegui-content,
        .nicegui-column {
            display: block !important;
            flex-direction: unset !important;
            align-items: unset !important;
            gap: 0 !important;
            padding: 0 !important;
        }
        section[style*="100vw"] {
            position: relative;
            left: 50%;
            right: 50%;
            margin-left: -50vw !important;
            margin-right: -50vw !important;
            width: 100vw !important;
            max-width: none !important;
        }
        .login-card {
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.95);
        }
        </style>
    """)
    
    # Header
    create_header()
    
    # Form state
    form_data = {
        "email": "",
        "password": "",
        "remember_me": False
    }
    
    def handle_login():
        """Handle login form submission"""
        if not form_data["email"] or not form_data["password"]:
            ui.notify("Please fill in all fields", type="negative")
            return
        
        result = auth_service.login(form_data["email"], form_data["password"])
        
        if result["success"]:
            ui.notify(f"Welcome back, {result['user']['name']}!", type="positive")
            
            # Redirect based on role
            if result["user"]["role"] == "vendor":
                ui.navigate.to("/vendor-dashboard")
            else:
                ui.navigate.to("/job-seeker-dashboard")
        else:
            ui.notify(result["message"], type="negative")
    
    # Hero Section
    with ui.element("section").classes("bg-gradient-to-br from-emerald-600 to-green-700 text-white py-20 min-h-screen flex items-center").style(
        "width: 100vw; margin-left: calc(-50vw + 50%);"
    ):
        with ui.element("div").classes("container mx-auto px-4"):
            with ui.row().classes("w-full items-center justify-center min-h-[60vh]"):
                
                # Left side - Welcome message
                with ui.column().classes("flex-1 max-w-lg pr-8 hidden md:block"):
                    ui.label("Welcome Back!").classes("text-5xl font-bold mb-6")
                    ui.label("Sign in to your account to continue managing your job postings or browsing opportunities.").classes("text-xl opacity-90 mb-8")
                    
                    # Features list
                    with ui.column().classes("space-y-4"):
                        with ui.row().classes("items-center space-x-3"):
                            ui.icon("list", size="md").classes("text-emerald-200")
                            ui.label("Manage your job postings").classes("text-lg")
                        
                        with ui.row().classes("items-center space-x-3"):
                            ui.icon("list", size="md").classes("text-emerald-200")
                            ui.label("Track applications and views").classes("text-lg")
                        
                        with ui.row().classes("items-center space-x-3"):
                            ui.icon("list", size="md").classes("text-emerald-200")
                            ui.label("Discover new opportunities").classes("text-lg")
                
                # Right side - Login form
                with ui.card().classes("login-card p-8 w-full max-w-md shadow-2xl border-0"):
                    with ui.column().classes("w-full space-y-6"):
                        
                        # Header
                        with ui.column().classes("text-center mb-6"):
                            ui.label("Sign In").classes("text-3xl font-bold text-gray-800 mb-2")
                            ui.label("Enter your credentials to access your account").classes("text-gray-600")
                        
                        # Email field
                        with ui.column().classes("space-y-2"):
                            ui.label("Email Address").classes("text-sm font-semibold text-gray-700")
                            email_input = ui.input(
                                placeholder="Enter your email",
                                on_change=lambda e: form_data.update({"email": e.value})
                            ).props("outlined dense prepend-icon=email").classes("w-full")
                        
                        # Password field
                        with ui.column().classes("space-y-2"):
                            ui.label("Password").classes("text-sm font-semibold text-gray-700")
                            password_input = ui.input(
                                placeholder="Enter your password",
                                password=True,
                                password_toggle_button=True,
                                on_change=lambda e: form_data.update({"password": e.value})
                            ).props("outlined dense prepend-icon=lock").classes("w-full")
                        
                        # Remember me and forgot password
                        with ui.row().classes("w-full justify-between items-center"):
                            ui.checkbox(
                                "Remember me",
                                on_change=lambda e: form_data.update({"remember_me": e.value})
                            ).classes("text-sm text-gray-600")
                            
                            ui.link("Forgot password?", "#").classes("text-sm text-emerald-600 hover:text-emerald-700 font-medium")
                        
                        # Login button
                        ui.button(
                            "Sign In",
                            on_click=handle_login,
                            color="#10b981"
                        ).props("unelevated size=lg").classes("w-full py-3 text-white font-semibold text-lg shadow-lg hover:shadow-xl transition-all")
                        
                        # Divider
                        with ui.row().classes("w-full items-center my-6"):
                            ui.element("div").classes("flex-1 h-px bg-gray-300")
                            ui.label("OR").classes("px-4 text-gray-500 text-sm")
                            ui.element("div").classes("flex-1 h-px bg-gray-300")
                        
                        # Social login buttons (placeholder)
                        with ui.row().classes("w-full space-x-3"):
                            ui.button(
                                "Google",
                                icon="login"
                            ).props("outline color=grey-8 size=md").classes("flex-1")
                            
                            ui.button(
                                "LinkedIn",
                                icon="business"
                            ).props("outline color=grey-8 size=md").classes("flex-1")
                        
                        # Sign up link
                        with ui.row().classes("w-full justify-center mt-6"):
                            ui.label("Don't have an account?").classes("text-gray-600")
                            ui.link("Sign up here", "/signup").classes("text-emerald-600 hover:text-emerald-700 font-semibold ml-1")
    
    # Demo credentials section
    with ui.element("section").classes("py-12 bg-gray-100"):
        with ui.element("div").classes("container mx-auto px-4 max-w-4xl"):
            with ui.card().classes("p-6 bg-blue-50 border border-blue-200"):
                ui.label("Demo Credentials").classes("text-xl font-bold text-blue-800 mb-4")
                
                with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-2 gap-6"):
                    # Vendor demo
                    with ui.column().classes("space-y-2"):
                        ui.label("Vendor Account").classes("font-semibold text-blue-700")
                        ui.label("Email: admin@test.com").classes("text-sm text-gray-700 font-mono")
                        ui.label("Password: admin123").classes("text-sm text-gray-700 font-mono")
                        ui.label("Access: Full vendor dashboard").classes("text-xs text-blue-600")
                    
                    # User demo
                    with ui.column().classes("space-y-2"):
                        ui.label("Regular User Account").classes("font-semibold text-blue-700")
                        ui.label("Create a new account with 'user' role").classes("text-sm text-gray-700")
                        ui.label("Access: Browse jobs only").classes("text-xs text-blue-600")
    
    # Footer
    create_footer()

    # Handle Enter key for login
    ui.keyboard(on_key=lambda e: handle_login() if e.key.name == 'Enter' else None)
