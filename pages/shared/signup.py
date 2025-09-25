"""
Signup Page - User Registration for Vendors and Users
"""

from nicegui import ui
from services.auth_service import auth_service
from components.header import create_header
from components.footer import create_footer

@ui.page("/signup")
def signup_page():
    """Create the signup page"""
    
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
        .signup-card {
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.95);
        }
        .role-selector {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .role-selector:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-color: #00b074 !important;
        }
        .role-selected {
            border-color: #00b074 !important;
            background-color: #f0fdf4 !important;
            box-shadow: 0 4px 15px rgba(0, 176, 116, 0.2) !important;
        }
        .role-selector .q-card__section {
            padding: 0 !important;
        }
        </style>
    """)
    
    # Header
    create_header()
    
    # Form state
    form_data = {
        "name": "",
        "email": "",
        "password": "",
        "confirm_password": "",
        "role": "job_seeker",  # Default to job_seeker
        "terms_accepted": False
    }
    
    def handle_signup():
        """Handle signup form submission with enhanced API support"""
        # Enhanced validation
        if not all([form_data["name"], form_data["email"], form_data["password"], form_data["confirm_password"]]):
            ui.notify("Please fill in all fields", type="negative")
            return
        
        # Validate email format
        if "@" not in form_data["email"] or "." not in form_data["email"]:
            ui.notify("Please enter a valid email address", type="negative")
            return
        
        # Password validation
        if form_data["password"] != form_data["confirm_password"]:
            ui.notify("Passwords do not match", type="negative")
            return
        
        if len(form_data["password"]) < 6:
            ui.notify("Password must be at least 6 characters long", type="negative")
            return
        
        # Password strength check
        if form_data["password"].isdigit() or form_data["password"].isalpha():
            ui.notify("Password should contain both letters and numbers for better security", type="warning")
        
        if not form_data["terms_accepted"]:
            ui.notify("Please accept the terms and conditions to continue", type="negative")
            return
        
        # Validate role selection (should always have a role, but double-check)
        if not form_data["role"]:
            ui.notify("Please select your account type", type="negative")
            return
        
        # Show confirmation with selected role
        role_display = "Employer/Vendor" if form_data["role"] == "vendor" else "Job Seeker"
        ui.notify(f"Creating your {role_display} account...", type="info")
        
        try:
            # Try API registration first
            result = auth_service.api_register_user(
                form_data["email"],
                form_data["password"],
                form_data["name"],
                form_data["role"]
            )
            
            if result["success"]:
                ui.notify("Account created successfully! Please log in with your new credentials.", type="positive")
                # Auto-navigate to login after successful registration
                ui.navigate.to("/login")
            else:
                # API registration failed, try fallback
                error_msg = result["message"]
                
                if "not available" in error_msg:
                    # API service not available, try local registration
                    ui.notify("API service unavailable, trying local registration...", type="info")
                    
                    fallback_result = auth_service.register_user(
                        form_data["email"],
                        form_data["password"],
                        form_data["name"],
                        form_data["role"]
                    )
                    
                    if fallback_result["success"]:
                        ui.notify("Account created locally! Please log in.", type="positive")
                        ui.navigate.to("/login")
                    else:
                        ui.notify(fallback_result["message"], type="negative")
                else:
                    # Handle specific API errors - ensure error_msg is a string
                    error_str = str(error_msg) if error_msg else "Unknown error"
                    error_lower = error_str.lower()
                    
                    if "already" in error_lower or "exist" in error_lower:
                        ui.notify("An account with this email already exists. Please try logging in instead.", type="warning")
                    elif "invalid" in error_lower:
                        ui.notify("Invalid registration data. Please check your information and try again.", type="negative")
                    else:
                        ui.notify(f"Registration failed: {error_str}", type="negative")
        
        except Exception as e:
            ui.notify(f"An unexpected error occurred during registration: {str(e)}", type="negative")
    
    def select_role(role: str):
        """Handle role selection with visual feedback"""
        # Update form data
        form_data["role"] = role
        
        # Remove selection styling from both cards
        vendor_card.classes(remove="role-selected")
        user_card.classes(remove="role-selected")
        
        # Add selection styling to the chosen card and update labels
        if role == "vendor":
            vendor_card.classes(add="role-selected")
            selected_role_label.set_text("Selected: Employer/Vendor")
            role_description.set_text("As an Employer, you'll be able to post unlimited job listings, manage applications, connect with talented candidates, and build your team.")
            ui.notify("You'll be able to post jobs and hire talent", type="info")
        else:  # job_seeker
            user_card.classes(add="role-selected") 
            selected_role_label.set_text("Selected: Job Seeker")
            role_description.set_text("As a Job Seeker, you'll be able to browse job listings, save favorite jobs, apply for positions, and track your application status.")
            ui.notify("You'll be able to browse and apply for jobs", type="info")
    
    # Hero Section
    with ui.element("section").classes("bg-gradient-to-br from-green-100 to-green-200 text-green-400 py-20 min-h-screen flex items-center").style(
        "width: 100vw; margin-left: calc(-50vw + 50%);"
    ):
        with ui.element("div").classes("container mx-auto px-4"):
            with ui.row().classes("w-full items-center justify-center min-h-[70vh]"):
                
                # Left side - Welcome message
                with ui.column().classes("flex-1 max-w-lg pr-8 hidden lg:block"):
                    ui.label("Join Our Platform!").classes("text-5xl font-bold mb-6 text-[#2b3940]")
                    ui.label("Create your account and start your journey with us today.").classes("text-xl mb-8 text-[#2b3940]")
                    
                    # Benefits list
                    with ui.column().classes("space-y-4"):
                        with ui.row().classes("items-center space-x-3"):
                            ui.icon("check_circle", size="md").classes("text-[#00b074]")
                            ui.label("Post unlimited job listings").classes("text-lg text-[#2b3940]")
                        
                        with ui.row().classes("items-center space-x-3"):
                            ui.icon("check_circle", size="md").classes("text-[#00b074]")
                            ui.label("Connect with top talent").classes("text-lg text-[#2b3940]")
                        
                        with ui.row().classes("items-center space-x-3"):
                            ui.icon("check_circle", size="md").classes("text-[#00b074]")
                            ui.label("Grow your business").classes("text-lg text-[#2b3940]")
                
                # Right side - Signup form
                with ui.card().classes("signup-card p-8 w-full max-w-lg shadow-2xl border-0"):
                    with ui.column().classes("w-full space-y-6"):
                        
                        # Header
                        with ui.column().classes("text-center mb-6"):
                            ui.label("Create Account").classes("text-3xl font-bold text-[#2b3940] mb-2")
                            ui.label("Choose your account type and get started").classes("text-[#2b3940]")
                        
                        # Role selection
                        with ui.column().classes("space-y-3"):
                            ui.label("I am a:").classes("text-sm font-semibold text-[#2b3940]")
                            ui.label("Choose your account type").classes("text-xs text-gray-600 mb-2")
                            
                            # Selected role display
                            selected_role_label = ui.label("Selected: Job Seeker").classes("text-xs text-[#00b074] font-medium mb-1")
                            
                            with ui.row().classes("w-full space-x-3"):
                                # Employer/Vendor option
                                with ui.card().classes("role-selector flex-1 p-4 cursor-pointer border-2 border-gray-300 hover:border-[#00b074] transition-all") as vendor_card:
                                    vendor_card.on('click', lambda: select_role('vendor'))
                                    with ui.column().classes("items-center text-center space-y-2"):
                                        ui.icon("business", size="lg").classes("text-[#00b074]")
                                        ui.label("Employer").classes("font-semibold text-[#2b3940]")
                                        ui.label("Post jobs & hire talent").classes("text-xs text-gray-600")
                                
                                # Job Seeker option (default selected)
                                with ui.card().classes("role-selector role-selected flex-1 p-4 cursor-pointer border-2 border-[#00b074] bg-green-50 transition-all") as user_card:
                                    user_card.on('click', lambda: select_role('job_seeker'))
                                    with ui.column().classes("items-center text-center space-y-2"):
                                        ui.icon("person_search", size="lg").classes("text-[#00b074]")
                                        ui.label("Job Seeker").classes("font-semibold text-[#2b3940]")
                                        ui.label("Find job opportunities").classes("text-xs text-gray-600")
                        
                        # Role description
                        with ui.card().classes("p-3 bg-blue-50 border border-blue-200"):
                            role_description = ui.label("As a Job Seeker, you'll be able to browse job listings, save favorite jobs, and apply for positions that match your skills.").classes("text-xs text-blue-700")
                        
                        # Name field
                        with ui.column().classes("space-y-2"):
                            ui.label("Full Name").classes("text-sm font-semibold text-[#2b3940]")
                            name_input = ui.input(
                                placeholder="Enter your full name",
                                on_change=lambda e: form_data.update({"name": e.value})
                            ).props("outlined dense prepend-icon=person").classes("w-full")
                        
                        # Email field
                        with ui.column().classes("space-y-2"):
                            ui.label("Email Address").classes("text-sm font-semibold text-[#2b3940]")
                            email_input = ui.input(
                                placeholder="Enter your email",
                                on_change=lambda e: form_data.update({"email": e.value})
                            ).props("outlined dense prepend-icon=email").classes("w-full")
                        
                        # Password field
                        with ui.column().classes("space-y-2"):
                            ui.label("Password").classes("text-sm font-semibold text-[#2b3940]")
                            password_input = ui.input(
                                placeholder="Create a password (min 6 characters)",
                                password=True,
                                password_toggle_button=True,
                                on_change=lambda e: form_data.update({"password": e.value})
                            ).props("outlined dense prepend-icon=lock").classes("w-full")
                        
                        # Confirm password field
                        with ui.column().classes("space-y-2"):
                            ui.label("Confirm Password").classes("text-sm font-semibold text-[#2b3940]")
                            confirm_password_input = ui.input(
                                placeholder="Confirm your password",
                                password=True,
                                on_change=lambda e: form_data.update({"confirm_password": e.value})
                            ).props("outlined dense prepend-icon=lock").classes("w-full")
                        
                        # Terms and conditions
                        with ui.row().classes("w-full items-start space-x-2"):
                            ui.checkbox(
                                on_change=lambda e: form_data.update({"terms_accepted": e.value})
                            )
                            with ui.column().classes("flex-1"):
                                ui.html("""
                                    <span class="text-sm text-[#2b3940]">
                                        I agree to the <a href="#" class="text-blue-600 hover:text-blue-700 font-medium">Terms of Service</a> 
                                        and <a href="#" class="text-blue-600 hover:text-blue-700 font-medium">Privacy Policy</a>
                                    </span>
                                """)
                        
                        # Signup button
                        ui.button(
                            "Create Account",
                            on_click=handle_signup,
                            color="#00b074"
                        ).props("unelevated size=lg").classes("w-full py-3 text-white font-semibold text-lg shadow-lg hover:shadow-xl transition-all")
                        
                        # Login link
                        with ui.row().classes("w-full justify-center mt-6"):
                            ui.label("Already have an account?").classes("text-gray-600")
                            ui.link("Sign in here", "/login").classes("text-blue-600 hover:text-blue-700 font-semibold ml-1")
    
    # Features section
    with ui.element("section").classes("py-16 bg-white flex items-center justify-center"):
        with ui.element("div").classes("container mx-auto px-4 max-w-6xl text-center"):
            ui.label("Why Choose Our Platform?").classes("text-3xl font-bold text-center justify-center text-gray-800 mb-12")
            
            with ui.row().classes("w-full justify-center items-center"):
                with ui.element("div").classes("grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto"):
                    # Feature 1
                    with ui.card().classes("p-6 text-center hover:shadow-lg transition-shadow mx-auto"):
                        ui.icon("speed", size="xl").classes("text-[#00b074] mb-4 mx-auto")
                        ui.label("Fast & Easy").classes("text-xl font-semibold text-gray-800 mb-3 text-center !important")
                        ui.label("Quick registration process gets you started in minutes").classes("text-gray-600 text-center")
                    
                    # Feature 2
                    with ui.card().classes("p-6 text-center hover:shadow-lg transition-shadow mx-auto"):
                        ui.icon("security", size="xl").classes("text-[#00b074] mb-4 mx-auto")
                        ui.label("Secure & Trusted").classes("text-xl font-semibold text-gray-800 mb-3 text-center")
                        ui.label("Your data is protected with enterprise-grade security").classes("text-gray-600 text-center")
                    
                    # Feature 3
                    with ui.card().classes("p-6 text-center hover:shadow-lg transition-shadow mx-auto"):
                        ui.icon("support_agent", size="xl").classes("text-[#00b074] mb-4 mx-auto")
                        ui.label("24/7 Support").classes("text-xl font-semibold text-gray-800 mb-3 text-center")
                        ui.label("Get help whenever you need it from our support team").classes("text-gray-600 text-center")
    
    # Footer
    create_footer()

    # Handle Enter key for signup
    ui.keyboard(on_key=lambda e: handle_signup() if e.key.name == 'Enter' else None)
