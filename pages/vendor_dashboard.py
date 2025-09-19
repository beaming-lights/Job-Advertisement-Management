from nicegui import ui
from services.api_service import APIService
from services.auth_service import auth_service
from typing import Optional
from components.header import create_header
from components.footer import create_footer

@ui.page("/vendor-dashboard")
def vendor_dashboard_page():
    """Vendor Dashboard - Protected route for vendors only"""
    
    # Check authentication and role
    if not auth_service.require_vendor("/login"):
        return
    # Add NiceGUI content override for full width layout and prevent horizontal scroll
    ui.add_head_html("""
    <style>
        /* Prevent horizontal scrolling */
        html, body {
            overflow-x: hidden !important;
            max-width: 100vw !important;
        }
        
        /* Enhanced scrollbar styling for table */
        .overflow-x-auto::-webkit-scrollbar {
            height: 12px;
        }
        
        .overflow-x-auto::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 6px;
        }
        
        .overflow-x-auto::-webkit-scrollbar-thumb {
            background: #00b074;
            border-radius: 6px;
            border: 2px solid #f1f5f9;
        }
        
        .overflow-x-auto::-webkit-scrollbar-thumb:hover {
            background: #059669;
        }
        
        /* Scroll shadow indicators */
        .scroll-container {
            position: relative;
        }
        
        .scroll-container::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 20px;
            height: 100%;
            background: linear-gradient(to left, rgba(0,0,0,0.1), transparent);
            pointer-events: none;
            z-index: 1;
        }
        
        /* NiceGUI Content Override - Force full width layout */
        .nicegui-content,
        .nicegui-column {
            display: block !important;
            flex-direction: unset !important;
            align-items: unset !important;
            gap: 0 !important;
            padding: 0 !important;
            overflow-x: hidden !important;
            max-width: 100vw !important;
        }
        
        /* Override page container constraints */
        .q-page-container, .q-layout, .q-page {
            padding: 0 !important;
            margin: 0 !important;
            width: 100vw !important;
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }
        
        /* Ensure all containers don't exceed viewport width */
        * {
            box-sizing: border-box !important;
        }
        
        .q-page, .nicegui-content, [class*="w-full"] {
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }
    </style>
    """)
    
    # Add header
    create_header()
    
    # Initialize API service
    api_service = APIService()
    
    # Page Header with Title
    with ui.element("div").classes("w-full bg-gradient-to-r from-[#00b074] to-[#009960] text-white py-16"):
        with ui.element("div").classes("container mx-auto px-8"):
            with ui.column().classes("items-center text-center"):
                ui.label("Vendor Dashboard").classes("text-5xl font-bold mb-4")
                ui.label("Manage your job postings and track applications").classes("text-xl opacity-90")
    
    # Main Content Container with proper spacing
    with ui.element("div").classes("container mx-auto px-8 py-8"):
        # Main Content with Side Navigation
        with ui.row().classes("w-full min-h-screen no-wrap gap-6"):
            # Left Navigation
            with ui.column().classes("w-1/4 bg-gray-100 p-6 space-y-2 rounded-lg shadow-sm"):
                ui.label("Dashboard").classes("text-xl font-bold p-2 mb-4")
                overview_button = (
                    ui.button(
                        "Overview",
                        icon="dashboard",
                        on_click=lambda: show_content("overview"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm")
                )
                settings_button = (
                    ui.button(
                        "Settings",
                        icon="settings",
                        on_click=lambda: show_content("settings"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm")
                )
                jobs_button = (
                    ui.button(
                        "Posted Jobs",
                        icon="work_history",
                        on_click=lambda: show_content("posted_jobs"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm")
                )
                applicants_button = (
                    ui.button(
                        "Applicants",
                        icon="people",
                        on_click=lambda: show_content("applicants"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm")
                )
                candidates_button = (
                    ui.button(
                        "Browse Candidates",
                        icon="person_search",
                        on_click=lambda: show_content("candidates"),
                    )
                    .props("flat dense align=left")
                    .classes("w-full text-sm")
                )

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
                    """Update button styles based on active section"""
                    overview_button.props(
                        'color="#00b074"' if active_section == "overview" else "color=default"
                    )
                    settings_button.props(
                        'color="#00b074"' if active_section == "settings" else "color=default"
                    )
                    jobs_button.props(
                        'color="#00b074"' if active_section == "posted_jobs" else "color=default"
                    )
                    applicants_button.props(
                        'color="#00b074"' if active_section == "applicants" else "color=default"
                    )
                    candidates_button.props(
                        'color="#00b074"' if active_section == "candidates" else "color=default"
                    )

                def show_content(section: str):
                    """Clear and show only the selected section content"""
                    current_section["value"] = section
                    main_content_container.clear()
                    update_button_styles(section)
                    
                    if section == "overview":
                        load_overview_content()
                    elif section == "settings":
                        load_settings_content()
                    elif section == "posted_jobs":
                        load_posted_jobs_content()
                    elif section == "applicants":
                        load_applicants_content()
                    elif section == "candidates":
                        load_candidates_content()

                def create_stat_card(icon, value, label, gradient_from, gradient_to):
                    """Helper function to create modern green-themed stat cards"""
                    with ui.card().classes("w-full p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 cursor-pointer border border-gray-100"):
                        with ui.row().classes("items-center space-x-5"):
                            # Modern gradient icon circle
                            with ui.element("div").classes(f"w-16 h-16 bg-gradient-to-br {gradient_from} {gradient_to} rounded-xl flex items-center justify-center shadow-lg"):
                                ui.icon(icon, size="1.75rem").classes("text-white")
                            
                            # Stats content
                            with ui.column().classes("space-y-1"):
                                ui.label(value).classes("text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent")
                                ui.label(label).classes("text-sm font-semibold text-gray-600 uppercase tracking-wide")

                def load_overview_content():
                    """Load overview section content"""
                    try:
                        jobs = api_service.get_jobs()
                        applicants = api_service.get_applicants()
                    except Exception as e:
                        print(f"Error loading overview data: {e}")
                        jobs = []
                        applicants = []

                    with main_content_container:
                        # Modern Green-themed Stats cards
                        with ui.row().classes(
                            "w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10"
                        ):
                            create_stat_card(
                                "work",
                                f"{len(jobs)}",
                                "Posted Jobs",
                                "from-emerald-500",
                                "to-green-600"
                            )
                            create_stat_card(
                                "people",
                                f"{len(applicants)}",
                                "Total Applicants",
                                "from-green-500",
                                "to-emerald-600"
                            )
                            create_stat_card(
                                "visibility", 
                                "16.5K", 
                                "Jobs View", 
                                "from-teal-500",
                                "to-green-600"
                            )
                            create_stat_card(
                                "trending_up",
                                "18.6%",
                                "Applied Rate",
                                "from-lime-500",
                                "to-emerald-600"
                            )

                        # Recent data section
                        with ui.row().classes(
                            "w-full grid grid-cols-1 lg:grid-cols-2 gap-8"
                        ):
                            with ui.column().classes("w-full"):
                                ui.label("Recent Job Postings").classes(
                                    "text-xl font-bold mb-4"
                                )
                                with ui.card().classes("w-full p-4"):
                                    if jobs:
                                        for job in jobs[:3]:
                                            with ui.row().classes(
                                                "w-full items-center border-b py-2"
                                            ):
                                                ui.label(job.get("title", "Unknown")).classes(
                                                    "font-semibold w-1/2"
                                                )
                                                ui.label(job.get("location", "N/A")).classes(
                                                    "text-gray-500 w-1/2"
                                                )
                                    else:
                                        ui.label("No jobs posted yet").classes("text-gray-500 text-center py-4")

                            with ui.column().classes("w-full"):
                                ui.label("Recent Applicants").classes(
                                    "text-xl font-bold mb-4"
                                )
                                with ui.card().classes("w-full p-4"):
                                    if applicants:
                                        for app in applicants[:3]:
                                            with ui.row().classes(
                                                "w-full items-center border-b py-3"
                                            ):
                                                with ui.column().classes("space-y-0"):
                                                    ui.label(app.get("name", "Unknown")).classes(
                                                        "font-semibold"
                                                    )
                                                    ui.label(app.get("job_title", "N/A")).classes(
                                                        "text-gray-500 text-sm"
                                                    )
                                    else:
                                        ui.label("No applicants yet").classes("text-gray-500 text-center py-4")

                def load_settings_content():
                    """Load settings section content with professional form layout"""
                    with main_content_container:
                        ui.label("Account Settings").classes("text-2xl font-bold text-gray-900 mb-6")
                        
                        with ui.row().classes("w-full gap-8"):
                            # Left column - Profile Settings
                            with ui.column().classes("w-2/3"):
                                with ui.card().classes("w-full bg-white shadow-sm rounded-lg p-8"):
                                    ui.label("Company Information").classes("text-lg font-semibold text-gray-900 mb-6")
                                    
                                    with ui.column().classes("space-y-6"):
                                        # Company name
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Company Name").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="Enter your company name").classes("w-full")
                                        
                                        # Email
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Email Address").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="Enter your email address").classes("w-full")
                                        
                                        # Phone
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Phone Number").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="Enter your phone number").classes("w-full")
                                        
                                        # Website
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Website URL").classes("text-sm font-medium text-gray-700")
                                            ui.input(placeholder="https://yourcompany.com").classes("w-full")
                                        
                                        # Company description
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Company Description").classes("text-sm font-medium text-gray-700")
                                            ui.textarea(placeholder="Tell us about your company...").classes("w-full h-24")
                                        
                                        # Modern action buttons
                                        with ui.row().classes("space-x-4 pt-6"):
                                            ui.button("Save Changes", color="#10b981").classes("px-8 py-3 font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all")
                                            ui.button("Cancel", color="gray").props("outline").classes("px-8 py-3 font-semibold rounded-lg hover:bg-gray-50 transition-all")
                            
                            # Right column - Additional Settings
                            with ui.column().classes("w-1/3"):
                                # Notification Settings
                                with ui.card().classes("w-full bg-white shadow-sm rounded-lg p-6 mb-6"):
                                    ui.label("Notification Settings").classes("text-lg font-semibold text-gray-900 mb-4")
                                    
                                    with ui.column().classes("space-y-4"):
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("Email Notifications").classes("text-sm text-gray-700")
                                            ui.switch().classes("")
                                        
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("New Applications").classes("text-sm text-gray-700")
                                            ui.switch(value=True).classes("")
                                        
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("Job Expiry Alerts").classes("text-sm text-gray-700")
                                            ui.switch(value=True).classes("")
                                
                                # Account Actions
                                with ui.card().classes("w-full bg-white shadow-sm rounded-lg p-6"):
                                    ui.label("Account Actions").classes("text-lg font-semibold text-gray-900 mb-4")
                                    
                                    with ui.column().classes("space-y-3"):
                                        ui.button("Change Password", color="#10b981").props("outline").classes("w-full font-semibold")
                                        ui.button("Download Data", color="gray").props("outline").classes("w-full font-semibold")
                                        ui.button("Delete Account", color="#ef4444").props("outline").classes("w-full font-semibold")

                def delete_job_handler(job_id: str, job_title: str):
                    """Handle job deletion with confirmation"""
                    def confirm_delete():
                        try:
                            success = api_service.delete_job(job_id)
                            if success:
                                ui.notify(f'Job "{job_title}" deleted successfully!', type='positive')
                                # Refresh the jobs list
                                load_posted_jobs_content()
                            else:
                                ui.notify('Failed to delete job. Please try again.', type='negative')
                        except Exception as e:
                            ui.notify(f'Error deleting job: {str(e)}', type='negative')
                        dialog.close()
                    
                    def cancel_delete():
                        dialog.close()
                    
                    # Create confirmation dialog
                    with ui.dialog() as dialog, ui.card().classes('w-96 p-6'):
                        ui.label('Confirm Deletion').classes('text-xl font-bold mb-4')
                        ui.label(f'Are you sure you want to delete "{job_title}"?').classes('text-gray-700 mb-6')
                        ui.label('This action cannot be undone.').classes('text-red-600 text-sm mb-6')
                        
                        with ui.row().classes('w-full justify-end space-x-3'):
                            ui.button('Cancel', on_click=cancel_delete).props('outline').classes('px-4 py-2')
                            ui.button('Delete', on_click=confirm_delete, color='#ef4444').classes('px-4 py-2 text-white')
                    
                    dialog.open()

                def edit_job_handler(job_data: dict):
                    """Handle job editing with inline edit dialog - using post-job form structure"""
                    # Normalize job type to match dropdown options
                    job_type_mapping = {
                        'full-time': 'Full-time',
                        'Full-time': 'Full-time', 
                        'Full-Time': 'Full-time',
                        'FULL-TIME': 'Full-time',
                        'part-time': 'Part-time',
                        'Part-time': 'Part-time',
                        'Part-Time': 'Part-time', 
                        'PART-TIME': 'Part-time',
                        'contract': 'Contract',
                        'Contract': 'Contract',
                        'CONTRACT': 'Contract',
                        'remote': 'Remote',
                        'Remote': 'Remote',
                        'REMOTE': 'Remote',
                        'internship': 'Internship',
                        'Internship': 'Internship',
                        'INTERNSHIP': 'Internship'
                    }
                    
                    # Parse existing salary range
                    salary_min = 0
                    salary_max = 0
                    if job_data.get('salary'):
                        try:
                            salary_parts = job_data.get('salary', '').replace('$', '').replace(',', '').split('-')
                            if len(salary_parts) == 2:
                                salary_min = int(salary_parts[0].strip())
                                salary_max = int(salary_parts[1].strip())
                        except:
                            pass
                    
                    # Normalize category to match dropdown options
                    category_options = ["Technology", "Marketing", "Sales", "Design", "Finance", "Operations"]
                    current_category = job_data.get('category', '')
                    
                    # Map common variations to standard options or default to Technology
                    category_mapping = {
                        'technology': 'Technology',
                        'tech': 'Technology',
                        'IT': 'Technology',
                        'marketing': 'Marketing',
                        'sales': 'Sales',
                        'design': 'Design',
                        'finance': 'Finance',
                        'operations': 'Operations',
                        'ops': 'Operations'
                    }
                    
                    # Normalize the category - if not found, default to Technology
                    normalized_category = category_mapping.get(current_category.lower(), 'Technology')
                    if current_category in category_options:
                        normalized_category = current_category
                    
                    # Create form state variables (similar to post-job page)
                    edit_form_data = {
                        'title': job_data.get('title', ''),
                        'company': job_data.get('company', ''),
                        'location': job_data.get('location', ''),
                        'job_type': job_type_mapping.get(job_data.get('job_type', ''), 'Full-time'),
                        'description': job_data.get('description', ''),
                        'requirements': job_data.get('requirements', ''),
                        'salary_min': salary_min,
                        'salary_max': salary_max,
                        'category': normalized_category,
                        'benefits': job_data.get('benefits', ''),
                        'contact_email': job_data.get('contact_email', ''),
                        'flyer_file': None,
                        'flyer_name': '',
                        'flyer_type': ''
                    }
                    
                    def handle_upload(e):
                        """Handle file upload (similar to post-job page)"""
                        edit_form_data["flyer_file"] = e.content
                        edit_form_data["flyer_name"] = e.name
                        edit_form_data["flyer_type"] = e.type
                        ui.notify(f"Prepared {e.name} for upload")

                    def save_job_changes():
                        """Save job changes (similar to post-job page)"""
                        try:
                            # Validate required fields
                            required_fields = ["title", "company", "location", "description"]
                            if not all(edit_form_data.get(field) for field in required_fields):
                                ui.notify("Please fill out all required fields.", type="negative")
                                return

                            # Map form data to API format (same as post-job page)
                            api_data = {
                                "job_title": edit_form_data.get("title"),
                                "company": edit_form_data.get("company"),
                                "job_description": edit_form_data.get("description"),
                                "category": edit_form_data.get("category"),
                                "job_type": edit_form_data.get("job_type"),
                                "location": edit_form_data.get("location"),
                                "min_salary": str(int(edit_form_data.get("salary_min", 0))),
                                "max_salary": str(int(edit_form_data.get("salary_max", 0))),
                                "benefits": edit_form_data.get("benefits", "Competitive benefits package"),
                                "requirements": edit_form_data.get("requirements", "Requirements will be discussed during interview"),
                                "date_posted": job_data.get('date_posted', '2024-01-15'),
                                "contact_email": edit_form_data.get("contact_email", "hr@company.com"),
                                "vendor_id": job_data.get('vendor_id', 'vendor_1')
                            }

                            # Handle file upload (same as post-job page)
                            flyer_file = None
                            if edit_form_data.get("flyer_file"):
                                class FileObject:
                                    pass
                                flyer_file = FileObject()
                                flyer_file.name = edit_form_data["flyer_name"]
                                flyer_file.content = edit_form_data["flyer_file"]
                                flyer_file.content_type = edit_form_data["flyer_type"]

                            # Update job using API
                            result = api_service.update_job(job_data.get('id'), api_data, file=flyer_file)
                            if result:
                                ui.notify("Job updated successfully!", type="positive")
                                dialog.close()
                                load_posted_jobs_content()  # Refresh the list
                            else:
                                ui.notify("Failed to update job. Please check the data and try again.", type="negative")
                        except Exception as e:
                            ui.notify(f'Error updating job: {str(e)}', type='negative')
                    
                    def handle_flyer_upload(e):
                        """Handle flyer image upload"""
                        try:
                            # Store the actual file object for API transmission
                            if hasattr(e, 'content') and hasattr(e, 'name'):
                                # Create a file-like object with the correct attributes
                                class FileUpload:
                                    def __init__(self, upload_event):
                                        self.name = upload_event.name
                                        self.content = upload_event.content
                                        self.content_type = getattr(upload_event, 'type', 'image/jpeg')
                                
                                flyer_data['file'] = FileUpload(e)
                                flyer_data['filename'] = e.name
                                flyer_data['content_type'] = getattr(e, 'type', 'image/jpeg')
                                flyer_data['has_file'] = True
                                ui.notify(f'Flyer "{e.name}" uploaded successfully!', type='positive')
                            else:
                                ui.notify('Failed to upload flyer. Please try again.', type='negative')
                        except Exception as ex:
                            ui.notify(f'Error uploading flyer: {str(ex)}', type='negative')
                    
                    def cancel_edit():
                        dialog.close()
                    
                    # Create edit dialog with post-job form structure
                    with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl p-8 max-h-[85vh] overflow-y-auto'):
                        ui.label(f'Edit Job: {job_data.get("title", "Unknown")}').classes('text-2xl font-bold mb-6 text-[#00b074]')
                        
                        with ui.column().classes('w-full space-y-8'):
                            # Section: Job Details
                            with ui.column().classes('w-full space-y-4'):
                                ui.label("Job Details").classes('text-xl font-bold mb-4 text-[#2b3940]')
                                with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-2 gap-6'):
                                    ui.input(
                                        "Job Title *",
                                        value=edit_form_data.get("title"),
                                        on_change=lambda e: edit_form_data.update({"title": e.value}),
                                    ).props("outlined dense")
                                    ui.input(
                                        "Company *",
                                        value=edit_form_data.get("company"),
                                        on_change=lambda e: edit_form_data.update({"company": e.value}),
                                    ).props("outlined dense")
                                    ui.input(
                                        "Location *",
                                        value=edit_form_data.get("location"),
                                        on_change=lambda e: edit_form_data.update({"location": e.value}),
                                    ).props("outlined dense")
                                    ui.input(
                                        "Contact Email",
                                        value=edit_form_data.get("contact_email"),
                                        on_change=lambda e: edit_form_data.update({"contact_email": e.value}),
                                    ).props("outlined dense")
                                    ui.textarea(
                                        "Job Description *",
                                        value=edit_form_data.get("description"),
                                        on_change=lambda e: edit_form_data.update({"description": e.value}),
                                    ).props("outlined dense")
                                    ui.textarea(
                                        "Requirements",
                                        value=edit_form_data.get("requirements"),
                                        on_change=lambda e: edit_form_data.update({"requirements": e.value}),
                                    ).props("outlined dense")
                                    ui.input(
                                        "Benefits",
                                        value=edit_form_data.get("benefits"),
                                        on_change=lambda e: edit_form_data.update({"benefits": e.value}),
                                    ).props("outlined dense")

                            # Section: Salary & Type
                            with ui.column().classes('w-full space-y-4'):
                                ui.label("Salary & Type").classes('text-xl font-bold text-[#2b3940] border-b pb-2')
                                with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-2 gap-6'):
                                    ui.input(
                                        "Min Salary",
                                        value=str(edit_form_data.get("salary_min", 0)),
                                        on_change=lambda e: edit_form_data.update({"salary_min": int(e.value) if e.value.isdigit() else 0}),
                                    ).props("outlined dense type=number prepend-icon=attach_money")
                                    ui.input(
                                        "Max Salary",
                                        value=str(edit_form_data.get("salary_max", 0)),
                                        on_change=lambda e: edit_form_data.update({"salary_max": int(e.value) if e.value.isdigit() else 0}),
                                    ).props("outlined dense type=number")
                                with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-2 gap-6'):
                                    ui.select(
                                        ["Technology", "Marketing", "Sales", "Design", "Finance", "Operations"],
                                        value=edit_form_data.get("category"),
                                        label="Category",
                                        on_change=lambda e: edit_form_data.update({"category": e.value}),
                                    ).props("outlined dense")
                                    ui.select(
                                        ["Full-time", "Part-time", "Contract", "Freelance", "Internship"],
                                        value=edit_form_data.get("job_type"),
                                        label="Job Type",
                                        on_change=lambda e: edit_form_data.update({"job_type": e.value}),
                                    ).props("outlined dense")

                            # Section: Job Flyer
                            with ui.column().classes('w-full space-y-4'):
                                ui.label("Job Flyer").classes('text-xl font-bold text-[#2b3940] border-b pb-2')
                                ui.upload(on_upload=handle_upload, auto_upload=True).props(
                                    "accept=.jpg,.jpeg,.png flat bordered"
                                ).classes("w-full")

                            # Action Buttons
                            with ui.row().classes('w-full justify-end space-x-4 pt-4'):
                                ui.button("Cancel", on_click=cancel_edit, color="grey-8").props("flat")
                                ui.button("Update Job", on_click=save_job_changes, color="#00b074").props("unelevated").style("color: white !important;")
                    
                    dialog.open()

                def load_posted_jobs_content():
                    """Load posted jobs section with a clean, modern table"""
                    try:
                        jobs = api_service.get_jobs()
                        
                        with main_content_container:
                            # Header Section
                            with ui.row().classes("w-full justify-between items-center mb-8"):
                                with ui.column():
                                    ui.label(f"Posted Jobs ({len(jobs)})").classes("text-3xl font-bold text-gray-900")
                                    ui.label("Manage and track your job postings").classes("text-gray-600 mt-2")
                                
                                # Action buttons
                                with ui.row().classes("space-x-3"):
                                  
                                    ui.button(
                                        "Post New Job",
                                        icon="add",
                                        on_click=lambda: ui.navigate.to("/post-job"),
                                        color="#00b074"
                                    ).props("unelevated").classes("text-white")
                            
                            if not jobs:
                                # Empty state
                                with ui.card().classes("w-full p-12 text-center bg-white shadow-lg rounded-xl"):
                                    ui.icon("work_off", size="4rem").classes("text-gray-300 mb-6")
                                    ui.label("No jobs posted yet").classes("text-2xl text-gray-600 mb-4 font-semibold")
                                    ui.label("Create your first job posting to get started").classes("text-gray-500 mb-6")
                                    ui.button(
                                        "Post Your First Job",
                                        icon="add_circle",
                                        on_click=lambda: ui.navigate.to("/post-job"),
                                        color="#00b074"
                                    ).props("unelevated size=lg").classes("px-8 py-3 text-white")
                            else:
                                # Jobs Table - Horizontally Scrollable
                                with ui.card().classes("w-full bg-white shadow-lg rounded-xl"):
                                    # Scroll hint
                                    with ui.element("div").classes("bg-blue-50 px-4 py-2 border-b border-blue-200"):
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label("Jobs Table").classes("font-semibold text-blue-800")
                                            ui.label("← Scroll horizontally to see all columns and actions →").classes("text-sm text-blue-600 italic")
                                    
                                    # Horizontal scroll container - simplified
                                    with ui.element("div").style("""
                                        overflow-x: auto; 
                                        overflow-y: hidden;
                                        width: 100%;
                                        max-width: 100%;
                                    """):
                                        with ui.element("table").style("width: 1400px; border-collapse: collapse; table-layout: fixed;"):
                                            # Table Header with fixed column widths
                                            with ui.element("thead"):
                                                with ui.element("tr").classes("bg-gradient-to-r from-green-50 to-emerald-50 border-b-2 border-green-200"):
                                                    with ui.element("th").classes("px-4 py-4 text-left text-sm font-bold text-green-800 uppercase tracking-wide border-r border-green-200").style("width: 250px; min-width: 250px;"):
                                                        ui.label("Job Title")
                                                    with ui.element("th").classes("px-4 py-4 text-left text-sm font-bold text-green-800 uppercase tracking-wide border-r border-green-200").style("width: 150px; min-width: 150px;"):
                                                        ui.label("Company")
                                                    with ui.element("th").classes("px-4 py-4 text-center text-sm font-bold text-green-800 uppercase tracking-wide border-r border-green-200").style("width: 150px; min-width: 150px;"):
                                                        ui.label("Type")
                                                    with ui.element("th").classes("px-4 py-4 text-center text-sm font-bold text-green-800 uppercase tracking-wide border-r border-green-200").style("width: 150px; min-width: 150px;"):
                                                        ui.label("Location")
                                                    with ui.element("th").classes("px-4 py-4 text-center text-sm font-bold text-green-800 uppercase tracking-wide border-r border-green-200").style("width: 180px; min-width: 180px;"):
                                                        ui.label("Salary")
                                                    with ui.element("th").classes("px-4 py-4 text-center text-sm font-bold text-green-800 uppercase tracking-wide border-r border-green-200").style("width: 100px; min-width: 100px;"):
                                                        ui.label("Posted")
                                                    with ui.element("th").classes("px-4 py-4 text-center text-sm font-bold text-green-800 uppercase tracking-wide border-r border-green-200").style("width: 80px; min-width: 80px;"):
                                                        ui.label("Status")
                                                    with ui.element("th").classes("px-4 py-4 text-center text-sm font-bold text-green-800 uppercase tracking-wide").style("width: 200px;"):
                                                        ui.label("Actions")
                                            
                                            # Table Body with fixed column widths
                                            with ui.element("tbody"):
                                                for i, job in enumerate(jobs):
                                                    row_bg = "bg-white" if i % 2 == 0 else "bg-gray-50"
                                                    
                                                    with ui.element("tr").classes(f"{row_bg} hover:bg-green-50 transition-colors duration-200 border-b border-gray-100").style("height: 60px;"):
                                                        # Job Title
                                                        with ui.element("td").classes("px-4 py-3 border-r border-gray-200").style("width: 250px;"):
                                                            ui.label(job.get("title", "Unknown Title")).classes("font-semibold text-gray-900 text-sm").style("white-space: nowrap; overflow: hidden; text-overflow: ellipsis;")
                                                        
                                                        # Company
                                                        with ui.element("td").classes("px-4 py-3 border-r border-gray-200").style("width: 150px;"):
                                                            ui.label(job.get("company", "N/A")).classes("text-gray-700 font-medium text-sm").style("white-space: nowrap; overflow: hidden; text-overflow: ellipsis;")
                                                        
                                                        # Job Type
                                                        with ui.element("td").classes("px-4 py-3 text-center border-r border-gray-200").style("width: 150px;"):
                                                            job_type = job.get("job_type", "N/A")
                                                            type_color = {
                                                                "Full-time": "bg-blue-100 text-blue-800",
                                                                "Part-time": "bg-yellow-100 text-yellow-800", 
                                                                "Contract": "bg-purple-100 text-purple-800",
                                                                "Freelance": "bg-green-100 text-green-800",
                                                                "Remote": "bg-indigo-100 text-indigo-800"
                                                            }.get(job_type, "bg-gray-100 text-gray-800")
                                                            
                                                            with ui.element("span").classes(f"inline-flex px-2 py-1 text-xs font-semibold rounded-full {type_color}"):
                                                                ui.label(job_type)
                                                        
                                                        # Location
                                                        with ui.element("td").classes("px-4 py-3 text-center border-r border-gray-200").style("width: 150px;"):
                                                            ui.label(job.get("location", "N/A")).classes("text-gray-700 text-sm").style("white-space: nowrap; overflow: hidden; text-overflow: ellipsis;")
                                                        
                                                        # Salary
                                                        with ui.element("td").classes("px-4 py-3 text-center border-r border-gray-200").style("width: 180px;"):
                                                            salary = job.get("salary", "N/A")
                                                            ui.label(salary).classes("text-gray-700 font-medium text-sm").style("white-space: nowrap; overflow: hidden; text-overflow: ellipsis;")
                                                        
                                                        # Posted Date
                                                        with ui.element("td").classes("px-4 py-3 text-center border-r border-gray-200").style("width: 100px;"):
                                                            posted_date = job.get("posted_date", "N/A")
                                                            ui.label(posted_date).classes("text-gray-600 text-xs")
                                                        
                                                        # Status
                                                        with ui.element("td").classes("px-4 py-3 text-center border-r border-gray-200").style("width: 80px;"):
                                                            with ui.element("span").classes("inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800"):
                                                                ui.label("Active")
                                                        
                                                        # Actions
                                                        with ui.element("td").classes("px-4 py-3 text-center").style("width: 200px;"):
                                                            with ui.row().classes("justify-center space-x-1"):
                                                                ui.button(
                                                                    "Edit", 
                                                                    
                                                                    on_click=lambda j=job: edit_job_handler(j),
                                                                    color="#00b074"
                                                                ).props("size=md dense").classes("text-sm text-white")
                                                                ui.button(
                                                                    "Delete",
                                                                  
                                                                    on_click=lambda j=job: delete_job_handler(j.get("id", ""), j.get("title", "Unknown Job")),
                                                                    color="red"
                                                                ).props("size=md outline dense").classes("text-sm")
                                
                                # Table Footer with Summary and Scroll Info
                                with ui.card().classes("w-full bg-gray-50 p-4 mt-4"):
                                    with ui.row().classes("w-full justify-between items-center"):
                                        with ui.column():
                                            ui.label(f"Showing {len(jobs)} job(s)").classes("text-sm text-gray-600")
                                            ui.label("Tip: Scroll horizontally in the table above to see all columns").classes("text-xs text-blue-600 mt-1")
                                        with ui.row().classes("space-x-4 items-center"):
                                            ui.label(f"Total Jobs: {len(jobs)}").classes("text-sm font-medium text-gray-700")
                                            active_jobs = len([j for j in jobs if j.get("status", "active").lower() == "active"])
                                            ui.label(f"Active: {active_jobs}").classes("text-sm font-medium text-green-600")
                                            ui.element("div").classes("w-2 h-2 bg-green-500 rounded-full animate-pulse")
                                    
                    except Exception as e:
                        with main_content_container:
                            ui.label("Error loading jobs").classes("text-xl text-red-600 mb-2")
                            ui.label(f"Details: {str(e)}").classes("text-gray-500")
                    

                def load_applicants_content():
                    """Load applicants section content"""
                    try:
                        applicants = api_service.get_applicants()
                    except Exception as e:
                        print(f"Error loading applicants: {e}")
                        applicants = []

                    with main_content_container:
                        ui.label("Applicants").classes("text-2xl font-bold mb-4")

                        if applicants:
                            for applicant in applicants:
                                with ui.card().classes("w-full p-4 mb-4"):
                                    ui.label(applicant.get("name", "Unknown")).classes("text-lg font-semibold")
                                    ui.label(applicant.get("job_title", "N/A")).classes("text-sm text-gray-600")
                                    ui.label(applicant.get("email", "N/A")).classes("text-sm text-gray-600")
                                    ui.label(applicant.get("status", "N/A")).classes("text-sm text-gray-600")
                        else:
                            ui.label("No applicants found.").classes("text-gray-500")

                def load_candidates_content():
                    """Load candidates browsing section content"""
                    try:
                        # For now, we'll use a mock candidates list - later this will come from API
                        candidates = [
                            {
                                "id": "1",
                                "name": "Sarah Johnson",
                                "title": "Senior Software Developer",
                                "location": "New York, NY",
                                "experience": "5+ years",
                                "skills": ["Python", "React", "Node.js", "AWS"],
                                "email": "sarah.johnson@email.com",
                                "phone": "+1 (555) 123-4567",
                                "availability": "Available",
                                "profile_image": "https://via.placeholder.com/100x100?text=SJ"
                            },
                            {
                                "id": "2", 
                                "name": "Michael Chen",
                                "title": "Full Stack Developer",
                                "location": "San Francisco, CA",
                                "experience": "3+ years",
                                "skills": ["JavaScript", "Vue.js", "PHP", "MySQL"],
                                "email": "michael.chen@email.com",
                                "phone": "+1 (555) 987-6543",
                                "availability": "Available in 2 weeks",
                                "profile_image": "https://via.placeholder.com/100x100?text=MC"
                            },
                            {
                                "id": "3",
                                "name": "Emily Rodriguez",
                                "title": "UI/UX Designer",
                                "location": "Austin, TX",
                                "experience": "4+ years",
                                "skills": ["Figma", "Adobe XD", "Sketch", "Prototyping"],
                                "email": "emily.rodriguez@email.com",
                                "phone": "+1 (555) 456-7890",
                                "availability": "Available",
                                "profile_image": "https://via.placeholder.com/100x100?text=ER"
                            }
                        ]
                    except Exception as e:
                        print(f"Error loading candidates: {e}")
                        candidates = []

                    with main_content_container:
                        # Header Section
                        with ui.row().classes("w-full justify-between items-center mb-8"):
                            with ui.column():
                                ui.label(f"Browse Candidates ({len(candidates)})").classes("text-3xl font-bold text-gray-900")
                                ui.label("Discover talented professionals for your opportunities").classes("text-gray-600 mt-2")
                            
                            # Search and Filter Controls
                            with ui.row().classes("space-x-3"):
                                ui.input(placeholder="Search candidates...").classes("w-64").props("outlined dense")
                                ui.select(
                                    options=["All Locations", "New York, NY", "San Francisco, CA", "Austin, TX", "Remote"],
                                    value="All Locations"
                                ).classes("w-48").props("outlined dense")
                                ui.select(
                                    options=["All Skills", "Python", "JavaScript", "React", "Node.js", "PHP", "Figma"],
                                    value="All Skills"
                                ).classes("w-48").props("outlined dense")

                        if not candidates:
                            # Empty state
                            with ui.card().classes("w-full p-12 text-center bg-white shadow-lg rounded-xl"):
                              
                                ui.label("No candidates found").classes("text-2xl text-gray-600 mb-4 font-semibold")
                                ui.label("Try adjusting your search filters").classes("text-gray-500 mb-6")
                        else:
                            # Candidates Grid - Clean Design
                            with ui.element("div").classes("grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"):
                                for candidate in candidates:
                                    # Clean Candidate Card
                                    with ui.card().classes("w-full bg-white shadow-sm rounded-lg hover:shadow-md transition-all duration-200 border border-gray-200"):
                                        with ui.column().classes("p-5 space-y-3"):
                                            # Simple Header
                                            with ui.column().classes("space-y-2"):
                                                ui.label(candidate["name"]).classes("font-semibold text-lg text-gray-900")
                                                ui.label(candidate["title"]).classes("text-sm text-gray-600")
                                                
                                                # Clean Availability
                                                availability_color = "text-green-700" if "Available" in candidate["availability"] else "text-yellow-700"
                                                ui.label(candidate["availability"]).classes(f"text-xs {availability_color} font-medium")
                                            
                                            # Location & Experience - Simple Layout
                                            with ui.column().classes("space-y-1"):
                                                ui.label(candidate["location"]).classes("text-sm text-gray-600")
                                                ui.label(candidate["experience"]).classes("text-sm text-gray-600")
                                            
                                            # Clean Skills Display
                                            with ui.column().classes("space-y-2"):
                                                ui.label("Skills").classes("text-sm font-medium text-gray-700")
                                                with ui.element("div").classes("flex flex-wrap gap-1"):
                                                    for skill in candidate["skills"][:3]:  # Show first 3 skills
                                                        with ui.element("span").classes("px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"):
                                                            ui.label(skill)
                                                    if len(candidate["skills"]) > 3:
                                                        with ui.element("span").classes("px-2 py-1 text-xs bg-gray-50 text-gray-500 rounded"):
                                                            ui.label(f"+{len(candidate['skills']) - 3}")
                                            
                                            # Simple Action Buttons
                                            with ui.row().classes("w-full space-x-2 pt-3 border-t border-gray-100"):
                                                ui.button(
                                                    "View",
                                                    on_click=lambda c=candidate: view_candidate_profile(c),
                                                    color="#00b074"
                                                ).props("outline size=sm").classes("flex-1")
                                                
                                                ui.button(
                                                    "Contact",
                                                    on_click=lambda c=candidate: contact_candidate(c),
                                                    color="#00b074"
                                                ).props("size=sm").classes("flex-1 text-white")

                def view_candidate_profile(candidate):
                    """View detailed candidate profile - Clean Design"""
                    with ui.dialog() as profile_dialog, ui.card().classes("w-full max-w-3xl"):
                        with ui.column().classes("p-8 space-y-8"):
                            # Clean Profile Header
                            with ui.column().classes("text-center pb-6 border-b border-gray-200"):
                                ui.label(candidate["name"]).classes("text-3xl font-bold text-gray-900 mb-2")
                                ui.label(candidate["title"]).classes("text-lg text-gray-600 mb-4")
                                
                                # Location & Experience - Simple Row
                                with ui.row().classes("justify-center space-x-8 text-sm text-gray-600"):
                                    ui.label(candidate["location"])
                                    ui.label("•").classes("text-gray-400")
                                    ui.label(candidate["experience"])
                                    ui.label("•").classes("text-gray-400")
                                    availability_color = "text-green-700" if "Available" in candidate["availability"] else "text-yellow-700"
                                    ui.label(candidate["availability"]).classes(f"{availability_color} font-medium")
                            
                            # Contact Information - Clean Layout
                            with ui.column().classes("space-y-4"):
                                ui.label("Contact Information").classes("text-xl font-semibold text-gray-900")
                                with ui.column().classes("space-y-2 bg-gray-50 p-4 rounded-lg"):
                                    with ui.row().classes("justify-between"):
                                        ui.label("Email").classes("text-sm font-medium text-gray-700")
                                        ui.label(candidate["email"]).classes("text-sm text-gray-900")
                                    
                                    with ui.row().classes("justify-between"):
                                        ui.label("Phone").classes("text-sm font-medium text-gray-700")
                                        ui.label(candidate["phone"]).classes("text-sm text-gray-900")
                            
                            # Skills Section - Minimal Design
                            with ui.column().classes("space-y-4"):
                                ui.label("Skills & Technologies").classes("text-xl font-semibold text-gray-900")
                                with ui.element("div").classes("flex flex-wrap gap-2"):
                                    for skill in candidate["skills"]:
                                        with ui.element("span").classes("px-3 py-2 text-sm bg-gray-100 text-gray-800 rounded-lg"):
                                            ui.label(skill)
                            
                            # Simple Action Buttons
                            with ui.row().classes("w-full justify-end space-x-3 pt-6 border-t border-gray-200"):
                                ui.button("Close", on_click=profile_dialog.close).props("flat").classes("px-6")
                                ui.button(
                                    "Send Message",
                                    on_click=lambda: contact_candidate(candidate),
                                    color="#00b074"
                                ).classes("text-white px-6")
                    
                    profile_dialog.open()

                def contact_candidate(candidate):
                    """Contact candidate functionality"""
                    ui.notify(f"Opening contact form for {candidate['name']}", type="info")
                    # Here you would implement the actual contact functionality

                # Set initial view and update todo
                show_content("overview")
    
    # Add footer
    create_footer()

