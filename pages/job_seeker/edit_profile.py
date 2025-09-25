from nicegui import ui

def candidate_edit_profile_page():
    """Simple edit profile page."""
    ui.page_title("Edit Profile")
    
    with ui.column().classes("gap-4 p-8"):
        ui.label("Edit Profile").classes("text-2xl font-bold")
        
        # Basic form
        ui.input("Full Name", placeholder="Enter your name")
        ui.input("Email", placeholder="Enter your email") 
        ui.input("Phone", placeholder="Enter your phone")
        ui.textarea("About", placeholder="Tell us about yourself")
        
        with ui.row().classes("gap-4"):
            ui.button("Save", on_click=lambda: ui.notify("Profile saved!"))
            ui.button("Cancel", on_click=lambda: ui.navigate.to("/candidate-profile"))
