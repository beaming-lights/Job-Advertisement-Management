"""
Job Seeker Dashboard Page
Displays an overview of saved jobs, recent applications, and recommended roles
"""

from nicegui import ui
from services.api_service import APIService
from services.auth_service import auth_service
from components.header import create_header
from components.footer import create_footer

@ui.page("/job-seeker-dashboard")
def job_seeker_dashboard_page():
    """Create the job seeker dashboard page"""
    
    # Check if user is authenticated - redirect to login if not
    print("Job Seeker Dashboard: Checking authentication...")
    if not auth_service.is_authenticated():
        print("Job Seeker Dashboard: User not authenticated, redirecting to login")
        ui.navigate.to("/login")
        return
    
    print("Job Seeker Dashboard: User authenticated, loading dashboard...")
    
    # Add CSS for proper layout
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
        </style>
    """)
    
    # Add header
    create_header()
    
    # Initialize API service
    api_service = APIService()
    
    # Page Header with Title
    with ui.element("div").classes("w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-16"):
        with ui.element("div").classes("container mx-auto px-8"):
            with ui.column().classes("items-center text-center"):
                ui.label("Job Seeker Dashboard").classes("text-5xl font-bold mb-4")
                ui.label("Your personalized job search experience").classes("text-xl opacity-90")
    
    # Main Content Container with proper spacing
    with ui.element("div").classes("container mx-auto px-8 py-8"):
        # Main Content with Side Navigation
        with ui.row().classes("w-full min-h-screen no-wrap gap-6"):
            # Left Navigation
            with ui.column().classes("w-1/4 bg-white p-6 space-y-3 rounded-xl shadow-lg border border-gray-100"):
                # Dashboard Header
                with ui.row().classes("items-center gap-3 mb-6"):
                    ui.icon("dashboard", size="1.5rem").classes("text-[#00b074]")
                    ui.label("Dashboard Menu").classes("text-xl font-bold text-gray-800")
                
                # Main Dashboard Navigation
                dashboard_button = (
                    ui.button(
                        "🏠 Dashboard Home",
                        icon="home",
                        on_click=lambda: show_content("overview"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm font-medium py-3 px-4 rounded-lg hover:bg-[#00b074] hover:text-white transition-all")
                )
                
                # Separator
                ui.separator().classes("my-3")
                
                # Job-related sections
                ui.label("Job Search").classes("text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 mb-2")
                
                overview_button = (
                    ui.button(
                        "📊 Overview",
                        icon="analytics",
                        on_click=lambda: show_content("overview"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-gray-100 transition-all")
                )
                saved_jobs_button = (
                    ui.button(
                        "🔖 Saved Jobs",
                        icon="bookmark",
                        on_click=lambda: show_content("saved_jobs"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-gray-100 transition-all")
                )
                applications_button = (
                    ui.button(
                        "💼 My Applications",
                        icon="work",
                        on_click=lambda: show_content("applications"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-gray-100 transition-all")
                )
                recommendations_button = (
                    ui.button(
                        "⭐ Recommendations",
                        icon="star",
                        on_click=lambda: show_content("recommendations"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-gray-100 transition-all")
                )
                
                # Separator
                ui.separator().classes("my-3")
                
                # Profile sections
                ui.label("Profile & Settings").classes("text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 mb-2")
                
                profile_button = (
                    ui.button(
                        "👤 My Profile",
                        icon="person",
                        on_click=lambda: ui.navigate.to("/candidate-profile"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-blue-100 hover:text-blue-700 transition-all")
                )
                edit_profile_button = (
                    ui.button(
                        "✏️ Edit Profile",
                        icon="edit",
                        on_click=lambda: ui.navigate.to("/candidate-edit-profile"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-blue-100 hover:text-blue-700 transition-all")
                )
                settings_button = (
                    ui.button(
                        "⚙️ Settings",
                        icon="settings",
                        on_click=lambda: show_content("settings"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-gray-100 transition-all")
                )
                
                # Quick Actions
                ui.separator().classes("my-3")
                ui.label("Quick Actions").classes("text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 mb-2")
                
                ui.button(
                    "🔍 Browse Jobs",
                    icon="search",
                    on_click=lambda: ui.navigate.to("/jobs"),
                ).props("flat dense align=left").classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-green-100 hover:text-green-700 transition-all")
                
                ui.button(
                    "📝 Update Resume",
                    icon="description",
                    on_click=lambda: ui.navigate.to("/candidate-edit-profile"),
                ).props("flat dense align=left").classes("w-full text-sm font-medium py-2 px-4 rounded-lg hover:bg-green-100 hover:text-green-700 transition-all")

            # Right Content Area
            with ui.column().classes("w-3/4 p-8 overflow-y-auto bg-white rounded-lg shadow-sm"):
                with ui.row().classes("w-full justify-between items-center mb-6"):
                    ui.label("Dashboard Overview").classes(
                        "text-3xl font-bold text-[#2b3940]"
                    )

                # Main content container that will be dynamically updated
                main_content_container = ui.column().classes("w-full")
                
                # Track current section
                current_section = {"value": "overview"}

                def update_button_styles(active_section: str):
                    """Update button styles based on active section with modern styling"""
                    # Remove active classes from all buttons first
                    buttons = [dashboard_button, overview_button, saved_jobs_button, applications_button, recommendations_button, settings_button]
                    for btn in buttons:
                        btn.classes(remove="bg-[#00b074] text-white shadow-lg")
                        btn.classes(add="hover:bg-gray-100")
                    
                    # Add active styling to the current section
                    active_button = None
                    if active_section == "overview":
                        active_button = dashboard_button
                    elif active_section == "saved_jobs":
                        active_button = saved_jobs_button
                    elif active_section == "applications":
                        active_button = applications_button
                    elif active_section == "recommendations":
                        active_button = recommendations_button
                    elif active_section == "settings":
                        active_button = settings_button
                    
                    if active_button:
                        active_button.classes(remove="hover:bg-gray-100")
                        active_button.classes(add="bg-[#00b074] text-white shadow-lg")
                    
                    # Profile buttons maintain their hover styles
                    profile_button.classes("hover:bg-blue-100 hover:text-blue-700")
                    edit_profile_button.classes("hover:bg-blue-100 hover:text-blue-700")

                def show_content(section: str):
                    """Clear and show only the selected section content"""
                    current_section["value"] = section
                    main_content_container.clear()
                    update_button_styles(section)
                    
                    if section == "overview":
                        load_overview_content()
                    elif section == "saved_jobs":
                        load_saved_jobs_content()
                    elif section == "applications":
                        load_applications_content()
                    elif section == "recommendations":
                        load_recommendations_content()
                    elif section == "settings":
                        load_settings_content()

                def load_overview_content():
                    """Load overview section content"""
                    try:
                        saved_jobs = api_service.get_saved_jobs()
                        applications = api_service.get_applications()
                        recommendations = api_service.get_recommendations()
                        print(f"Loaded data - Saved jobs: {len(saved_jobs)}, Applications: {len(applications)}, Recommendations: {len(recommendations)}")
                    except Exception as e:
                        print(f"Error loading overview data: {e}")
                        saved_jobs = []
                        applications = []
                        recommendations = []

                    with main_content_container:
                        # Overview of saved jobs, applications, and recommendations
                        ui.label("Quick Overview").classes("text-2xl font-bold mb-4")
                        
                        # Display saved jobs
                        ui.label("Saved Jobs").classes("text-lg font-semibold mb-2")
                        if saved_jobs:
                            for job in saved_jobs:
                                ui.label(f"- {job.get('title', 'Unknown')}").classes("text-sm")
                        else:
                            ui.label("No saved jobs.").classes("text-gray-500")

                        # Display recent applications
                        ui.label("Recent Applications").classes("text-lg font-semibold mt-4 mb-2")
                        if applications:
                            for app in applications:
                                ui.label(f"- {app.get('job_title', 'Unknown')} at {app.get('company', 'N/A')}").classes("text-sm")
                        else:
                            ui.label("No recent applications.").classes("text-gray-500")

                        # Display recommended roles
                        ui.label("Recommended Roles").classes("text-lg font-semibold mt-4 mb-2")
                        if recommendations:
                            for role in recommendations:
                                ui.label(f"- {role.get('title', 'Unknown')}").classes("text-sm")
                        else:
                            ui.label("No recommendations available.").classes("text-gray-500")

                def load_saved_jobs_content():
                    """Load saved jobs section content"""
                    try:
                        saved_jobs = api_service.get_saved_jobs()
                    except Exception as e:
                        print(f"Error loading saved jobs: {e}")
                        saved_jobs = []

                    with main_content_container:
                        ui.label("Saved Jobs").classes("text-2xl font-bold mb-6")
                        
                        if saved_jobs:
                            with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"):
                                for job in saved_jobs:
                                    with ui.card().classes("w-full p-6 hover:shadow-lg transition-shadow"):
                                        # Job header
                                        ui.label(job.get("title", "Unknown")).classes("text-lg font-bold mb-2")
                                        ui.label(job.get("company", "N/A")).classes("text-md text-gray-600 mb-2")
                                        ui.label(job.get("location", "N/A")).classes("text-sm text-gray-500 mb-3")
                                        
                                        # Job details
                                        ui.label(f"Salary: {job.get('salary', 'Not specified')}").classes("text-sm mb-2")
                                        ui.label(f"Type: {job.get('job_type', 'N/A')}").classes("text-sm mb-4")
                                        
                                        # Action buttons
                                        with ui.row().classes("w-full justify-between"):
                                            ui.button("View Details", color="#00b074").props("outline size=sm")
                                            ui.button("Remove", color="#ef4444").props("outline size=sm")
                        else:
                            with ui.card().classes("w-full p-8 text-center"):
                                ui.icon("bookmark_border", size="3rem").classes("text-gray-400 mb-4")
                                ui.label("No saved jobs yet").classes("text-xl text-gray-500 mb-2")
                                ui.label("Start browsing jobs and save the ones you're interested in!").classes("text-gray-400")
                                ui.button("Browse Jobs", on_click=lambda: ui.navigate.to("/jobs"), color="#00b074").classes("mt-4")

                def load_applications_content():
                    """Load applications section content"""
                    try:
                        applications = api_service.get_applications()
                    except Exception as e:
                        print(f"Error loading applications: {e}")
                        applications = []

                    with main_content_container:
                        ui.label("My Applications").classes("text-2xl font-bold mb-6")
                        
                        # Status filter buttons
                        with ui.row().classes("w-full mb-6 space-x-2"):
                            ui.button("All", color="#00b074").props("size=sm")
                            ui.button("Applied", color="gray").props("outline size=sm")
                            ui.button("Interview", color="blue").props("outline size=sm")
                            ui.button("Offer", color="green").props("outline size=sm")
                            ui.button("Rejected", color="red").props("outline size=sm")
                        
                        if applications:
                            with ui.column().classes("w-full space-y-4"):
                                for app in applications:
                                    with ui.card().classes("w-full p-6"):
                                        with ui.row().classes("w-full justify-between items-start"):
                                            # Application details
                                            with ui.column().classes("flex-1"):
                                                ui.label(app.get("job_title", "Unknown")).classes("text-lg font-bold mb-1")
                                                ui.label(app.get("company", "N/A")).classes("text-md text-gray-600 mb-2")
                                                ui.label(f"Applied on: {app.get('applied_date', 'N/A')}").classes("text-sm text-gray-500")
                                                ui.label(f"Resume used: {app.get('resume_name', 'Default Resume')}").classes("text-sm text-gray-500")
                                            
                                            # Status badge
                                            status = app.get("status", "applied").lower()
                                            status_colors = {
                                                "applied": "bg-blue-100 text-blue-800",
                                                "interview": "bg-yellow-100 text-yellow-800", 
                                                "offer": "bg-green-100 text-green-800",
                                                "rejected": "bg-red-100 text-red-800"
                                            }
                                            status_color = status_colors.get(status, "bg-gray-100 text-gray-800")
                                            
                                            with ui.element("div").classes(f"px-3 py-1 rounded-full text-sm font-medium {status_color}"):
                                                ui.label(status.title())
                                        
                                        # Action buttons
                                        with ui.row().classes("w-full mt-4 space-x-2"):
                                            ui.button("View Job", color="#00b074").props("outline size=sm")
                                            ui.button("View Resume", color="gray").props("outline size=sm")
                                            if status == "interview":
                                                ui.button("Schedule Interview", color="blue").props("size=sm")
                        else:
                            with ui.card().classes("w-full p-8 text-center"):
                                ui.icon("work_outline", size="3rem").classes("text-gray-400 mb-4")
                                ui.label("No applications yet").classes("text-xl text-gray-500 mb-2")
                                ui.label("Start applying to jobs to track your progress here!").classes("text-gray-400")
                                ui.button("Browse Jobs", on_click=lambda: ui.navigate.to("/jobs"), color="#00b074").classes("mt-4")

                def load_recommendations_content():
                    """Load recommendations section content with AI-powered suggestions"""
                    try:
                        recommendations = api_service.get_recommendations()
                        user_profile = api_service.get_user_profile()
                    except Exception as e:
                        print(f"Error loading recommendations: {e}")
                        recommendations = []
                        user_profile = {}

                    with main_content_container:
                        ui.label("AI-Powered Job Recommendations").classes("text-2xl font-bold mb-6")
                        
                        # AI recommendation explanation
                        with ui.card().classes("w-full p-4 mb-6 bg-blue-50 border border-blue-200"):
                            ui.label("🤖 Smart Recommendations").classes("text-lg font-semibold text-blue-800 mb-2")
                            ui.label("Based on your skills, experience, and job preferences, our AI has found these perfect matches for you.").classes("text-blue-700")
                        
                        if recommendations:
                            with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-2 gap-6"):
                                for job in recommendations:
                                    with ui.card().classes("w-full p-6 hover:shadow-lg transition-shadow border-l-4 border-green-500"):
                                        # Match score
                                        match_score = job.get("match_score", 85)
                                        with ui.row().classes("w-full justify-between items-center mb-3"):
                                            ui.label(job.get("title", "Unknown")).classes("text-lg font-bold")
                                            with ui.element("div").classes("bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm font-medium"):
                                                ui.label(f"{match_score}% Match")
                                        
                                        ui.label(job.get("company", "N/A")).classes("text-md text-gray-600 mb-2")
                                        ui.label(job.get("location", "N/A")).classes("text-sm text-gray-500 mb-3")
                                        
                                        # Why recommended
                                        ui.label("Why this matches you:").classes("text-sm font-semibold text-gray-700 mb-1")
                                        reasons = job.get("match_reasons", ["Skills alignment", "Experience level", "Location preference"])
                                        for reason in reasons[:3]:
                                            ui.label(f"• {reason}").classes("text-sm text-gray-600")
                                        
                                        # Action buttons
                                        with ui.row().classes("w-full mt-4 space-x-2"):
                                            ui.button("View Details", color="#00b074").props("size=sm")
                                            ui.button("Save Job", color="gray").props("outline size=sm")
                                            ui.button("Apply Now", color="#10b981").props("size=sm")
                        else:
                            with ui.card().classes("w-full p-8 text-center"):
                                ui.icon("psychology", size="3rem").classes("text-gray-400 mb-4")
                                ui.label("Building your recommendations...").classes("text-xl text-gray-500 mb-2")
                                ui.label("Complete your profile to get personalized job recommendations!").classes("text-gray-400")
                                ui.button("Complete Profile", color="#00b074").classes("mt-4")
                        
                        # Career insights section
                        ui.label("Career Insights").classes("text-xl font-bold mt-8 mb-4")
                        with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-3 gap-4"):
                            # Skill gap analysis
                            with ui.card().classes("w-full p-4"):
                                ui.label("🎯 Skill Gaps").classes("text-lg font-semibold mb-2")
                                ui.label("React, Node.js").classes("text-sm text-gray-600 mb-2")
                                ui.button("View Courses", color="#00b074").props("outline size=sm")
                            
                            # Salary benchmark
                            with ui.card().classes("w-full p-4"):
                                ui.label("💰 Salary Benchmark").classes("text-lg font-semibold mb-2")
                                ui.label("$75K - $95K").classes("text-sm text-gray-600 mb-2")
                                ui.button("View Details", color="#00b074").props("outline size=sm")
                            
                            # Trending skills
                            with ui.card().classes("w-full p-4"):
                                ui.label("📈 Trending Skills").classes("text-lg font-semibold mb-2")
                                ui.label("AI/ML, Cloud Computing").classes("text-sm text-gray-600 mb-2")
                                ui.button("Learn More", color="#00b074").props("outline size=sm")

                def load_settings_content():
                    """Load settings section content"""
                    with main_content_container:
                        ui.label("Account Settings").classes("text-2xl font-bold mb-6")
                        
                        with ui.row().classes("w-full gap-8"):
                            # Left column - Profile Settings
                            with ui.column().classes("w-2/3"):
                                with ui.card().classes("w-full bg-white shadow-sm rounded-lg p-8"):
                                    ui.label("Personal Information").classes("text-lg font-semibold text-gray-900 mb-6")
                                    
                                    with ui.column().classes("space-y-6"):
                                        # Full name
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Full Name").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="Enter your full name").classes("w-full")
                                        
                                        # Email
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Email Address").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="Enter your email address").classes("w-full")
                                        
                                        # Phone
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Phone Number").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="Enter your phone number").classes("w-full")
                                        
                                        # Location
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Location").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="City, State/Country").classes("w-full")
                                        
                                        # Bio
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Professional Bio").classes("text-sm font-medium text-gray-700")
                                            ui.textarea(placeholder="Tell us about yourself...").classes("w-full h-24")
                                        
                                        # Skills
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Skills").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="e.g., Python, JavaScript, React (comma separated)").classes("w-full")
                                        
                                        # Links
                                        with ui.row().classes("w-full space-x-4"):
                                            with ui.column().classes("flex-1 space-y-2"):
                                                ui.label("GitHub Profile").classes("text-sm font-medium text-gray-700")
                                                ui.input(placeholder="https://github.com/username").classes("w-full")
                                            
                                            with ui.column().classes("flex-1 space-y-2"):
                                                ui.label("LinkedIn Profile").classes("text-sm font-medium text-gray-700")
                                                ui.input(placeholder="https://linkedin.com/in/username").classes("w-full")
                                        
                                        # Resume upload
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Resume").classes("text-sm font-medium text-gray-700")
                                            ui.upload(auto_upload=True).props("accept=.pdf,.doc,.docx flat bordered").classes("w-full")
                                            ui.label("Upload your latest resume (PDF, DOC, DOCX)").classes("text-xs text-gray-500")
                                        
                                        # Action buttons
                                        with ui.row().classes("space-x-4 pt-6"):
                                            ui.button("Save Changes", color="#10b981").classes("px-8 py-3 font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all")
                                            ui.button("Cancel", color="gray").props("outline").classes("px-8 py-3 font-semibold rounded-lg hover:bg-gray-50 transition-all")
                            
                            # Right column - Preferences & Security
                            with ui.column().classes("w-1/3"):
                                # Job Preferences
                                with ui.card().classes("w-full bg-white shadow-sm rounded-lg p-6 mb-6"):
                                    ui.label("Job Preferences").classes("text-lg font-semibold text-gray-900 mb-4")
                                    
                                    with ui.column().classes("space-y-4"):
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Preferred Job Type").classes("text-sm font-medium text-gray-700")
                                            ui.select(["Full-time", "Part-time", "Contract", "Freelance", "Internship"], multiple=True).classes("w-full")
                                        
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Salary Range").classes("text-sm font-medium text-gray-700")
                                            with ui.row().classes("w-full space-x-2"):
                                                ui.input(placeholder="Min").classes("flex-1")
                                                ui.input(placeholder="Max").classes("flex-1")
                                        
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("Remote Work").classes("text-sm text-gray-700")
                                            ui.switch().classes("")
                                        
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("Willing to Relocate").classes("text-sm text-gray-700")
                                            ui.switch().classes("")
                                
                                # Notification Settings
                                with ui.card().classes("w-full bg-white shadow-sm rounded-lg p-6 mb-6"):
                                    ui.label("Notifications").classes("text-lg font-semibold text-gray-900 mb-4")
                                    
                                    with ui.column().classes("space-y-4"):
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("Email Notifications").classes("text-sm text-gray-700")
                                            ui.switch(value=True).classes("")
                                        
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("Job Recommendations").classes("text-sm text-gray-700")
                                            ui.switch(value=True).classes("")
                                        
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("Application Updates").classes("text-sm text-gray-700")
                                            ui.switch(value=True).classes("")
                                
                                # Account Security
                                with ui.card().classes("w-full bg-white shadow-sm rounded-lg p-6"):
                                    ui.label("Account Security").classes("text-lg font-semibold text-gray-900 mb-4")
                                    
                                    with ui.column().classes("space-y-3"):
                                        ui.button("Change Password", color="#10b981").props("outline").classes("w-full font-semibold")
                                        ui.button("Two-Factor Auth", color="gray").props("outline").classes("w-full font-semibold")
                                        ui.button("Download Data", color="gray").props("outline").classes("w-full font-semibold")
                                        ui.button("Delete Account", color="#ef4444").props("outline").classes("w-full font-semibold")

                # Initialize with overview content
                load_overview_content()
                update_button_styles("overview") 

    # Add footer
    create_footer()
