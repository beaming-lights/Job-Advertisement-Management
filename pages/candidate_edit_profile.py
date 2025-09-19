from nicegui import ui

def candidate_edit_profile_page():
    """Candidate edit profile page with comprehensive form fields."""
    
    # Set page title
    ui.page_title("Edit Profile - JobBoard")
    
    # Add page-specific CSS
    ui.add_head_html("""
    <style>
    body {
        overflow-x: hidden !important;
    }
    .edit-profile-card {
        background: white;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 0;
    }
    .form-section {
        border-bottom: 1px solid #e9ecef;
        padding: 2rem 0;
    }
    .form-section:last-child {
        border-bottom: none;
    }
    .skill-input-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .skill-tag-editable {
        background: #e8f5e8;
        color: #16a085;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        border: 1px solid #16a085;
    }
    .remove-skill {
        cursor: pointer;
        color: #dc3545;
        font-weight: bold;
    }
    .experience-form-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .add-button {
        background: #16a085;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .add-button:hover {
        background: #138d75;
    }
    .remove-button {
        background: #dc3545;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.875rem;
    }
    .green-button {
        background: #16a085 !important;
        color: white !important;
        border: none !important;
    }
    .green-button:hover {
        background: #138d75 !important;
    }
    .cancel-button {
        background: #6c757d !important;
        color: white !important;
        border: 1px solid #6c757d !important;
    }
    .cancel-button:hover {
        background: #5a6268 !important;
    }
    </style>
    """)
    
    # Form data storage
    form_data = {
        "personal": {
            "name": "David Henricks",
            "title": "Senior Product Designer", 
            "email": "david.henricks@email.com",
            "phone": "+1 (555) 123-4567",
            "location": "New York, USA",
            "website": "www.davidhenricks.com"
        },
        "about": "A talented professional with an academic background in Design and proven commercial development experience as a Product Designer since 2015.",
        "skills": ["UI/UX Design", "Figma", "Sketch", "Adobe Creative Suite", "Prototyping"],
        "experience": [
            {
                "title": "Lead Product Designer",
                "company": "Airbnb", 
                "start_date": "2020-06",
                "end_date": "Present",
                "location": "San Francisco, USA",
                "description": "Led design team for core product features"
            }
        ],
        "education": [
            {
                "degree": "Masters in Design",
                "institution": "Stanford University",
                "start_date": "2014",
                "end_date": "2016", 
                "location": "Stanford, USA"
            }
        ]
    }
    
    # Main container
    with ui.element("div").classes("min-h-screen bg-gray-50 py-8"):
        with ui.element("div").classes("container mx-auto px-4 max-w-4xl"):
            
            # Header
            with ui.row().classes("items-center justify-between mb-8"):
                ui.label("Edit Profile").classes("text-3xl font-bold text-gray-900")
                with ui.row().classes("gap-4"):
                    ui.button("Cancel", 
                        on_click=lambda: ui.navigate.to("/candidate-profile")).classes(
                        "cancel-button px-6 py-2 rounded-lg")
                    ui.button("Save Changes", 
                        on_click=save_profile).classes(
                        "green-button px-6 py-2 rounded-lg")
            
            with ui.card().classes("edit-profile-card p-8"):
                
                # Personal Information Section
                with ui.column().classes("form-section"):
                    ui.label("Personal Information").classes("text-xl font-bold text-gray-900 mb-6")
                    
                    with ui.row().classes("gap-6 w-full"):
                        name_input = ui.input("Full Name", value=form_data["personal"]["name"]).classes("flex-1")
                        title_input = ui.input("Professional Title", value=form_data["personal"]["title"]).classes("flex-1")
                    
                    with ui.row().classes("gap-6 w-full mt-4"):
                        email_input = ui.input("Email", value=form_data["personal"]["email"]).classes("flex-1")
                        phone_input = ui.input("Phone", value=form_data["personal"]["phone"]).classes("flex-1")
                    
                    with ui.row().classes("gap-6 w-full mt-4"):
                        location_input = ui.input("Location", value=form_data["personal"]["location"]).classes("flex-1")
                        website_input = ui.input("Website", value=form_data["personal"]["website"]).classes("flex-1")
                
                # About Section
                with ui.column().classes("form-section"):
                    ui.label("About").classes("text-xl font-bold text-gray-900 mb-6")
                    about_input = ui.textarea("About Me", value=form_data["about"]).classes("w-full").props("rows=5")
                
                # Skills Section
                with ui.column().classes("form-section"):
                    ui.label("Skills").classes("text-xl font-bold text-gray-900 mb-6")
                    
                    # Skills container
                    skills_container = ui.element("div").classes("skill-input-container")
                    
                    # Add skill input
                    with ui.row().classes("gap-4 items-end mt-4"):
                        new_skill_input = ui.input("Add Skill", placeholder="e.g., Python, JavaScript").classes("flex-1")
                        ui.button("Add Skill", 
                            on_click=lambda: add_skill(new_skill_input.value, skills_container, new_skill_input)).classes("green-button px-6 py-2 rounded-lg")
                    
                    # Display existing skills
                    def render_skills():
                        skills_container.clear()
                        with skills_container:
                            for skill in form_data["skills"]:
                                with ui.element("span").classes("skill-tag-editable"):
                                    ui.label(skill)
                                    remove_btn = ui.element("span").classes("remove-skill")
                                    remove_btn.text = "×"
                                    remove_btn.on("click", lambda s=skill: remove_skill(s, skills_container))
                    
                    def add_skill(skill_name, container, input_field):
                        if skill_name and skill_name not in form_data["skills"]:
                            form_data["skills"].append(skill_name)
                            input_field.set_value("")
                            render_skills()
                    
                    def remove_skill(skill_name, container):
                        if skill_name in form_data["skills"]:
                            form_data["skills"].remove(skill_name)
                            render_skills()
                    
                    render_skills()
                
                # Work Experience Section
                with ui.column().classes("form-section"):
                    ui.label("Work Experience").classes("text-xl font-bold text-gray-900 mb-6")
                    
                    experience_container = ui.column().classes("w-full")
                    
                    def render_experience():
                        experience_container.clear()
                        with experience_container:
                            for i, exp in enumerate(form_data["experience"]):
                                with ui.element("div").classes("experience-form-card"):
                                    with ui.row().classes("items-center justify-between mb-4"):
                                        ui.label(f"Experience #{i+1}").classes("font-semibold text-gray-700")
                                        if len(form_data["experience"]) > 1:
                                            ui.button("Remove", 
                                                on_click=lambda idx=i: remove_experience(idx)).classes("remove-button")
                                    
                                    with ui.row().classes("gap-4 w-full mb-4"):
                                        ui.input("Job Title", value=exp["title"]).classes("flex-1")
                                        ui.input("Company", value=exp["company"]).classes("flex-1")
                                    
                                    with ui.row().classes("gap-4 w-full mb-4"):
                                        ui.input("Start Date", value=exp["start_date"], placeholder="YYYY-MM").classes("flex-1")
                                        ui.input("End Date", value=exp["end_date"], placeholder="YYYY-MM or Present").classes("flex-1")
                                    
                                    ui.input("Location", value=exp["location"]).classes("w-full mb-4")
                                    ui.textarea("Description", value=exp.get("description", "")).classes("w-full").props("rows=3")
                    
                    def add_experience():
                        form_data["experience"].append({
                            "title": "",
                            "company": "",
                            "start_date": "",
                            "end_date": "",
                            "location": "",
                            "description": ""
                        })
                        render_experience()
                    
                    def remove_experience(index):
                        if len(form_data["experience"]) > 1:
                            form_data["experience"].pop(index)
                            render_experience()
                    
                    render_experience()
                    
                    ui.button("Add Experience", on_click=add_experience).classes("green-button px-6 py-2 rounded-lg mt-4")
                
                # Education Section
                with ui.column().classes("form-section"):
                    ui.label("Education").classes("text-xl font-bold text-gray-900 mb-6")
                    
                    education_container = ui.column().classes("w-full")
                    
                    def render_education():
                        education_container.clear()
                        with education_container:
                            for i, edu in enumerate(form_data["education"]):
                                with ui.element("div").classes("experience-form-card"):
                                    with ui.row().classes("items-center justify-between mb-4"):
                                        ui.label(f"Education #{i+1}").classes("font-semibold text-gray-700")
                                        if len(form_data["education"]) > 1:
                                            ui.button("Remove", 
                                                on_click=lambda idx=i: remove_education(idx)).classes("remove-button")
                                    
                                    with ui.row().classes("gap-4 w-full mb-4"):
                                        ui.input("Degree", value=edu["degree"]).classes("flex-1")
                                        ui.input("Institution", value=edu["institution"]).classes("flex-1")
                                    
                                    with ui.row().classes("gap-4 w-full mb-4"):
                                        ui.input("Start Year", value=edu["start_date"], placeholder="YYYY").classes("flex-1")
                                        ui.input("End Year", value=edu["end_date"], placeholder="YYYY").classes("flex-1")
                                    
                                    ui.input("Location", value=edu["location"]).classes("w-full")
                    
                    def add_education():
                        form_data["education"].append({
                            "degree": "",
                            "institution": "",
                            "start_date": "",
                            "end_date": "",
                            "location": ""
                        })
                        render_education()
                    
                    def remove_education(index):
                        if len(form_data["education"]) > 1:
                            form_data["education"].pop(index)
                            render_education()
                    
                    render_education()
                    
                    ui.button("Add Education", on_click=add_education).classes("green-button px-6 py-2 rounded-lg mt-4")
                
                # Social Links Section
                with ui.column().classes("form-section"):
                    ui.label("Social Links").classes("text-xl font-bold text-gray-900 mb-6")
                    
                    with ui.row().classes("gap-6 w-full"):
                        ui.input("LinkedIn", placeholder="https://linkedin.com/in/username").classes("flex-1")
                        ui.input("GitHub", placeholder="https://github.com/username").classes("flex-1")
                    
                    with ui.row().classes("gap-6 w-full mt-4"):
                        ui.input("Twitter", placeholder="https://twitter.com/username").classes("flex-1")
                        ui.input("Portfolio", placeholder="https://portfolio.com").classes("flex-1")
            
            # Save/Cancel buttons at bottom
            with ui.row().classes("justify-end gap-4 mt-8"):
                ui.button("Cancel", 
                    on_click=lambda: ui.navigate.to("/candidate-profile")).classes(
                    "cancel-button px-8 py-3 rounded-lg")
                ui.button("Save Changes", 
                    on_click=save_profile).classes(
                    "green-button px-8 py-3 rounded-lg")

def save_profile():
    """Save the profile data (in real app, this would save to database)."""
    ui.notify("Profile saved successfully!", type="positive")
    # In a real application, you would save form_data to your database here
    ui.navigate.to("/candidate-profile")
