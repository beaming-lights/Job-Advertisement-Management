from importlib import reload
from nicegui import ui, app
from services.api_service import APIService
from components.header import create_header
from components.hero import create_hero
from components.footer import create_footer

# Import from reorganized structure
from pages.vendor.dashboard import vendor_dashboard_page
from pages.vendor.post_job import post_job_page
from pages.job_seeker.dashboard import job_seeker_dashboard_page
from pages.job_seeker.profile import candidate_profile_page
from pages.job_seeker.edit_profile import candidate_edit_profile_page
from pages.shared.login import login_page
from pages.shared.signup import signup_page
from pages.shared.jobs import jobs_page
from pages.shared.home import home_page
from components.job_details_modal import show_job_details
from services.auth_service import auth_service
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
import base64

# Load environment variables
load_dotenv()

# Initialize API service
api_service = APIService()


@ui.page("/")
def index():
    """Main page for the JobBoard website."""
    # Header
    create_header()

    # Hero Section
    create_hero()

    # Home page content
    home_page()

    # Footer
    create_footer()


# Route definitions
@ui.page("/vendor-dashboard")
def vendor_dashboard():
    """Vendor dashboard page with role-based access control."""
    # Check if user is authenticated and has vendor/employer role
    current_user = auth_service.get_current_user()
    if not current_user:
        ui.navigate.to("/login")
        return
    
    user_role = current_user.get("role", "")
    if user_role not in ["vendor", "employer"]:
        ui.notify("Access denied. This page is for vendors/employers only.", type="negative")
        ui.navigate.to("/")
        return
    
    create_header()
    vendor_dashboard_page()
    create_footer()


@ui.page("/post-job")
def post_job():
    """Post job page with role-based access control."""
    # Check if user is authenticated and has vendor/employer role
    current_user = auth_service.get_current_user()
    if not current_user:
        ui.navigate.to("/login")
        return
    
    user_role = current_user.get("role", "")
    if user_role not in ["vendor", "employer"]:
        ui.notify("Access denied. Only vendors/employers can post jobs.", type="negative")
        ui.navigate.to("/")
        return
    
    create_header()
    post_job_page()
    create_footer()


@ui.page("/job-seeker-dashboard")
def job_seeker_dashboard():
    """Job seeker dashboard page with authentication check."""
    # Check if user is authenticated
    current_user = auth_service.get_current_user()
    if not current_user:
        ui.navigate.to("/login")
        return
    
    # Any authenticated user can access job seeker dashboard
    # but redirect vendors to their own dashboard
    user_role = current_user.get("role", "")
    if user_role in ["vendor", "employer"]:
        ui.navigate.to("/vendor-dashboard")
        return
    
    create_header()
    job_seeker_dashboard_page()
    create_footer()


@ui.page("/jobs")
def jobs():
    """Jobs listing page."""
    create_header()
    jobs_page()
    create_footer()


@ui.page("/login")
def login():
    """Login page."""
    login_page()


@ui.page("/signup")
def signup():
    """Signup page."""
    signup_page()


@ui.page("/candidate-profile")
def candidate_profile():
    """Candidate profile page with authentication check."""
    # Check if user is authenticated
    current_user = auth_service.get_current_user()
    if not current_user:
        ui.navigate.to("/login")
        return
    
    create_header()
    candidate_profile_page()
    create_footer()


@ui.page("/candidate-edit-profile")
def candidate_edit_profile():
    """Candidate edit profile page with authentication check."""
    # Check if user is authenticated
    current_user = auth_service.get_current_user()
    if not current_user:
        ui.navigate.to("/login")
        return
    
    create_header()
    candidate_edit_profile_page()
    create_footer()


@ui.page("/admin-dashboard")
def admin_dashboard():
    """Admin dashboard page with admin-only access."""
    # Check if user is authenticated and has admin role
    current_user = auth_service.get_current_user()
    if not current_user:
        ui.navigate.to("/login")
        return
    
    user_role = current_user.get("role", "")
    if user_role != "admin":
        ui.notify("Access denied. This page is for administrators only.", type="negative")
        ui.navigate.to("/")
        return
    
    create_header()
    
    # Simple admin dashboard placeholder
    with ui.element("section").classes("py-20 bg-gray-50 min-h-screen"):
        with ui.element("div").classes("container mx-auto px-4"):
            ui.label("Admin Dashboard").classes("text-4xl font-bold text-center text-gray-800 mb-8")
            ui.label("Administrator panel for managing users and system settings").classes("text-xl text-center text-gray-600 mb-12")
            
            with ui.card().classes("p-8 max-w-4xl mx-auto"):
                ui.label("Welcome to the admin area! This is a placeholder for admin functionality.").classes("text-lg text-gray-700")
                ui.label(f"Logged in as: {current_user.get('name', 'Admin')}").classes("text-sm text-gray-600 mt-4")
    
    create_footer()


if __name__ in {"__main__", "__mp_main__"}:
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    
    # Add CSS to fix NiceGUI spacing issues
    ui.add_head_html('''
    <style>
    .nicegui-content,
    .nicegui-column {
        display: block !important;
        flex-direction: unset !important;
        align-items: unset !important;
        gap: 0 !important;
        padding: 0 !important;
    }
    </style>
    ''')

    # Get secure storage secret from environment variables
    storage_secret = os.getenv(
        "STORAGE_SECRET", "dev-fallback-secret-change-in-production"
    )

    ui.run(
        title="JobBoard - Modern Job Portal",
        port=int(os.getenv("PORT", 8080)),
        host="0.0.0.0",
        storage_secret=storage_secret,
        show=True,
        reload=True,
    )
